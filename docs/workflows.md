# GitHub Actions Workflows

This document describes each GitHub Actions workflow in `.github/workflows/`.

## Table of Contents

- [Overview](#overview)
- [Test](#test)
  - [Debugging pytest hangs after django.setup()](#debugging-pytest-hangs-after-djangosetup)
- [Publish](#publish)
- [Build](#build)
- [Sync env to server](#sync-env-to-server)
- [Static Files](#static-files)
- [Branch Protection](#branch-protection)
- [Labeler](#labeler)

## Overview

Workflows are split by responsibility: tests run on every change; publishing runs on push to `main` or version tags (`v*`) via a single Publish workflow; branch protection and labeler run on pull requests. Reusable workflows (`test`, `build-and-push`, `static-files`) can be called by others or triggered manually. Workflows that use environment vars or secrets run a **check-vars-and-secrets** job first (script: `scripts/check-workflow-env.sh`) where applicable; it fails if any required value passed to the script is missing (**Test** checks **Variables** only; disposable DB values for pytest are set in the workflow).

**Versioning**: Application version is derived from git tags (e.g., `v0.3.4` → `0.3.4`). See [Versioning Strategy](versioning.md) for details.

## Test

**File:** `.github/workflows/test.yml`

Runs the full test suite with pytest.

**Triggers:**

- **Pull request** targeting `main` or `develop`
- **Callable** by other workflows via **`workflow_call`** (optional **`test_path`** input)

**Jobs:** **pre-commit** – checkout, Python 3.14, `pip install -e ".[dev]"`, `pre-commit run --all-files` (see [docs/ci/python-project-standards.md](ci/python-project-standards.md)); **check-vars-and-secrets** – validates required **GitHub Variables** (no **`DB_APP_*`** / **`DB_SUPERUSER_PASSWORD`** / **`DJANGO_SECRET_KEY`** / **`TMTA_USERNAME`** secrets for pytest: the **pytest** job injects the same disposable defaults as [`docker-compose.yml`](../docker-compose.yml) — **`htmt_api`**, **`htmt_api_user`** / **`htmt_api_password`**, superuser **`postgres`**, **`DJANGO_SECRET_KEY=dev-only-secret-key`**, and workflow-level **`TMTA_USERNAME=tmta`**); **pytest** (Pytest) – checkout → lowercase **`GHCR_IMAGE_NAMESPACE`** → **`docker logout ghcr.io`** then **`docker login ghcr.io`** (**`GITHUB_TOKEN`** as lowercase **`GITHUB_REPOSITORY_OWNER`**, job **`packages: read`**) so **`afp`** pulls are authenticated (avoids **`unauthorized`** on private/internal GHCR images). Optional secrets **`GHCR_READ_PACKAGES_USERNAME`** / **`GHCR_READ_PACKAGES_TOKEN`** (classic PAT) if **`GITHUB_TOKEN`** still cannot pull until the **`afp`** package grants this repo **Read** under **Package → Actions access** → build **`api`** → pull **`db`** / **`afp`** → **`docker compose up --wait`** → **`docker compose run api`** (pytest + JUnit on workspace mount) → publish test results → teardown.

**Environment:** `ci_test` (repository/org **Variables** for image paths and app naming; optional **`GHCR_READ_PACKAGES_*`** secrets for **`afp`** pulls only).

**GHCR `afp` image and CI `unauthorized`:** Container images live under **GitHub Packages**, not under the source repo’s **Settings → General** page. To grant **`hear-the-music-tree-api`** workflows read access: open the org’s packages list (**[BehindTheMusicTree → Packages](https://github.com/orgs/BehindTheMusicTree/packages)**), click the **`audio-fingerprinter`** container (name may match the image), then **Package settings** → **Actions access** → **Add repository** → **`BehindTheMusicTree/hear-the-music-tree-api`** with **Read**. Alternatively, from the **`audio-fingerprinter`** code repo home page, use the **Packages** section in the right-hand sidebar (if the package is linked to the repo) to jump to the same package page. Repository visibility (**public** / private) is separate from **package** visibility; a public repo can still publish a **private** GHCR image.

**Versioning:** Always uses "test" as the version (tests don't require real version numbers).

### Debugging pytest hangs after django.setup()

If the job prints Django lines ending around **`apps.populate() finished`** / **`django.setup() is finishing`** and then **no further output for many minutes**, treat it as a **real stall** in the pytest startup chain (not only a missing log line).

1. **Use the full job log** (GitHub Actions: raw log or download). Search for:
   - `ci_pytest_startup_plugin` — **`outer enter`** without **`outer leave`** means the process is stuck **inside** the rest of `pytest_load_initial_conftests` (after `django.setup()`, before that hook finishes).
   - `api/test/conftest.py: imported` — confirms initial conftest import ran.
2. **Probe step:** The pytest job runs **`pytest --show-ini`** and **`pytest --trace-config`** (truncated) **before** the main `pytest` invocation so you can confirm **`inifile`**, **`rootdir`**, **`addopts`**, and registered plugins.
3. **Environment (set in `test.yml` for `docker compose run`):**
   - **`CI_STARTUP_TRACE=1`** — enables verbose `[Django]` / `[pytest]` diagnostics in application code.
   - **`PYTEST_PLUGINS=api.ci_pytest_startup_plugin`** — loads the hook-bracket plugin even when a bind-mount hides image-local `*.egg-info` entry points.
   - **`PYTHONFAULTHANDLER=1`** — on hang, send **SIGQUIT** to the pytest process (e.g. from another shell: `docker kill -s QUIT <container>` or `kill -QUIT <pid>`) to dump Python stacks to stderr.
4. **Repo / image:** `pytest.ini` is **not** listed in `.dockerignore` so the Docker build context includes it; the workflow still bind-mounts the workspace for JUnit output.

For local reproduction with the same diagnostics: `CI_STARTUP_TRACE=1 PYTEST_PLUGINS=api.ci_pytest_startup_plugin PYTHONFAULTHANDLER=1 docker compose exec api pytest api/test/ …`

## Publish

**File:** `.github/workflows/publish.yml`

Single publish workflow: collect static files, build Docker image, set image tags on server (API, DB, AFP) via shared workflows, then trigger redeployment webhook. Destination and env are chosen from the trigger.

**Triggers:**

- **Push** to `main` → **TEST** env, deploy to staging (image tag `staging`, app version from `VERSION` file + `-staging`)
- **Push** of version tags (`v*`) → **TEST** if prerelease (version contains `-`, e.g. `v0.2.0-rc1`, `v1.0.0-dev`), **PROD** if release (e.g. `v0.2.0`)
- **workflow_dispatch** (run from chosen branch)
- **workflow_call** (from other workflows; uses latest git tag when not on `main` or a tag ref)

**Jobs:**

1. **determine-version** – from ref: main → staging + TEST; tag with `-` → TEST; tag without `-` → PROD
2. **static** – calls `static-files.yml`, commits and pushes collected static files
3. **build-and-push** – calls `build-and-push.yml` with commit hash and **environment** (TEST or PROD)
4. **check-pinned-tags** – requires **`AFP_VERSION`** in Settings → Variables (no `latest`); DB image is **`postgres:16.4`** (fixed in [`docker-compose.yml`](../docker-compose.yml); publish sets server DB tag **`16.4`**)
5. **set-version-api** / **set-version-db** / **set-version-afp** – shared workflows from `BehindTheMusicTree/github-workflows`
6. **redeploy-webhook-call** – shared workflow **`call-redeployment-webhook`** (pinned **`@v1.0.1`**) with required **`hook_id_base: ${{ vars.REDEPLOYMENT_HOOK_ID_BASE }}`** and **`secrets: inherit`**

**Environment:** **TEST** for main push and prerelease/dev tags (staging). **PROD** for release tags (production). DB and AFP image tags must be pinned in repo variables.

**Variables (org-level pool, same as Sync env):** `REDEPLOYMENT_ROOT` (e.g. `/var/webhook/redeployment`). Set once at the **organization** (Settings → Variables) so the infrastructure repo and all app repos that call set-image-tag-on-server use the same path. If unset, the tag file path is wrong and the step fails.

**Versioning:** Main push uses `VERSION` file and tag `staging`. Tag push uses tag version; `workflow_call` without a tag uses latest git tag.

**Migrations:** Not run by the workflow. The API container entrypoint runs `migrate` after the database is ready.

## Build And Push

**File:** `.github/workflows/build-and-push.yml`

Builds the app Docker image and pushes it to **GitHub Container Registry** (`ghcr.io`).

**Triggers:**

- **Callable** via `workflow_call` (optional `commit_hash`; optional `environment`, default `TEST`; used by Publish)

**Jobs:** **build-and-push-to-ghcr** – checkout at ref → login to `ghcr.io` with **`GITHUB_TOKEN`** → build and push image with build-args from repo vars. Uses **environment** (TEST or PROD) for vars. Workflow declares **`permissions: packages: write`**.

**Environment:** Dynamic from caller: **TEST** or **PROD**. Image ref: **`ghcr.io/<GHCR_IMAGE_NAMESPACE>/<HTMT_API_IMAGE_REPO>:<IMAGE_TAG>`** (namespace must match **BehindTheMusicTree/infrastructure** variable **`GHCR_IMAGE_NAMESPACE`**). Remove **`DOCKERHUB_USERNAME`** / **`DOCKERHUB_ACCESS_TOKEN`**; set variable **`GHCR_IMAGE_NAMESPACE`** (lowercase org or user).

## Sync env to server

**File:** `.github/workflows/sync-env-to-server.yml`

Manually sync app env vars and secrets for **both STAGING and PROD** in one run. The workflow builds **two** fragments per env: **API** (Django/OAuth/app secrets → **`/tmp/sync-env-<HTMT_API_APP_NAME>-<env>.env`**) and **Postgres** (**`POSTGRES_*`** → **`/tmp/sync-env-<HTMT_API_APP_NAME><DB_APP_NAME_SUFFIX>-<env>.env`**, with **`DB_APP_NAME_SUFFIX`** required and non-empty — must match **BehindTheMusicTree/infrastructure**, often **`_db`**). The shared **`sync-env-to-server`** workflow uploads each fragment; **`redeploy-btmt-containers.sh`** promotes both into **`scripts/sync-env/`**, and **`generate-docker-compose.sh`** loads the API file then the DB file. **`FILE_UPLOAD_ENABLED`**, **`SPOTIFY_ENABLED`**, **`GOOGLE_OAUTH_ENABLED`**, **`MUSICBRAINZ_LOOKUP_ENABLED`**, and **`HTMT_API_AFP_ENABLED`** are **hardcoded `true`** in the API fragment (no GitHub Variables). **Jobs:** **build-api-fragment** / **build-db-fragment** (matrix STAGING + PROD), **sync-api-\***, **sync-db-\***. No `workflow_dispatch` inputs; one run syncs both environments.

**Triggers:** **workflow_dispatch** (Actions → Sync env to server → Run workflow). No inputs.

**Secrets (this repo, per environment):** `DB_APP_DB_NAME`, `DB_APP_USERNAME`, `DB_APP_USER_PASSWORD`, `DB_SUPERUSER_PASSWORD`, `DEMO_PASSWORD`, `DEMO_USERNAME`, `DJANGO_SECRET_KEY`, `GOOGLE_CLIENT_SECRET`, `SPOTIFY_CLIENT_SECRET`, `SUPERADMIN_PASSWORD`, `SUPERADMIN_USERNAME`, `TMTA_USERNAME`, plus deploy secrets `SERVER_DEPLOY_USERNAME`, `SERVER_DEPLOY_SSH_PRIVATE_KEY`.

**Variables (this repo or org, per GitHub Environment):** `SERVER_HOST`, `REDEPLOYMENT_ROOT`, `SYNC_ENV_REMOTE_FILENAME_PREFIX_BASE`, `HTMT_API_APP_NAME`, **`DB_APP_NAME_SUFFIX`** (required, non-empty; must match **BehindTheMusicTree/infrastructure**, e.g. `_db`), `DEMO_EMAIL`, `SUPERADMIN_EMAIL`, `SPOTIFY_CLIENT_ID_STAGING`, `SPOTIFY_CLIENT_ID_PROD`, `GOOGLE_CLIENT_ID_STAGING`, `GOOGLE_CLIENT_ID_PROD`, **`SPOTIFY_SCOPES`** (see `env/dev/.env.dev.example`). The compose-required API booleans above are **not** Variables—they are written as **`true`** in the workflow. Locally and in CI you still set **`FILE_UPLOAD_ENABLED`** in `.env` as needed (see `api/settings.py` / `TMP_UPLOADED_FILES`).

## Static Files

**File:** `.github/workflows/static-files.yml`

Collects Django static files and commits/pushes them back to the repo.

**Triggers:**

- **Callable** via `workflow_call` (used by Publish)

**Jobs:** **check-vars-and-secrets** (Check vars and secrets) – determines version from git tags and validates required env vars and secrets; **collect-and-push-static-files** (Static files) – Checkout → set up Python 3.14 → install deps → setup filesystem → `manage.py collectstatic --noinput` with version from job 1 → git config → commit and push changes → output `collect_static_files_commit_hash` and `app_version` for downstream workflows.

**Environment:** `collect_static`. Outputs are used by Publish so Build uses the commit that includes collected static files and the correct version.

**Django `ENV`:** The workflow sets **`ENV=collect_static`** on the job (see `api/settings.py`); it is **not** read from a GitHub Variable.

**Runtime staging / production:** Values such as **`ENV=prod`** (or your chosen string) for containers on the VPS belong in [**BehindTheMusicTree/infrastructure**](https://github.com/BehindTheMusicTree/infrastructure)—generated or merged **`scripts/.env`**, compose templates, sync jobs—not in this app repo’s GitHub Variables. This repo only hard-codes **`ENV` for CI-only workflows** (`ci_test` in **Test**, **`collect_static`** here).

## Branch Protection

**File:** `.github/workflows/branch-protection.yml`

Enforces Git Flow: only allows certain source branches for PRs to `main` and `develop`.

**Triggers:**

- **Pull request** targeting `main` or `develop`

**Jobs:** **check-branch-name** (Verify PR source branch) – validates source branch against target per Git Flow; **actionlint** (Actionlint) – lints workflow files.

**Logic:**

- **PRs to `main`:** source branch must be `hotfix/*` or `release/*`; otherwise the job fails
- **PRs to `develop`:** source branch must be `feature/*`, `chore/*`, `dependabot/*`, or `release/*`; otherwise the job fails (classic Git Flow uses `feature/*`; other prefixes here are documented in CONTRIBUTING.md under **Branch Protection**).

**No manual or workflow_call;** runs only on PR open/sync.

### Required status checks (branch protection)

Configure branch protection to require the **exact check names** that GitHub Actions reports (workflow name + job name). In **Settings → Branches → Branch protection rule** (for `main` and/or `develop`), under "Require status checks to pass before merging", enable **Require status checks to pass before merging** and in the search box add these four checks (type or select each):

1. **Test / Pytest**
2. **Test / Check vars and secrets**
3. **Branch Protection Check / Actionlint**
4. **Branch Protection Check / Verify PR source branch**

Checks appear in the dropdown only after they have run **successfully at least once in the past 7 days**. See [GitHub: Troubleshooting required status checks](https://docs.github.com/en/pull-requests/collaborating-with-pull-requests/collaborating-on-repositories-with-code-quality-features/troubleshooting-required-status-checks).

## Labeler

**File:** `.github/workflows/labeler.yml`

Adds labels to pull requests based on changed files using `.github/labeler.yml`.

**Triggers:**

- **Pull request** events: `opened`, `synchronize`, `reopened`, `labeled`, `unlabeled`

**Jobs:** **label** (Auto Label PR) – Checkout (full depth) → run `actions/labeler@v5` with `sync-labels: true`.

**Permissions:** `contents: read`, `pull-requests: write`.
