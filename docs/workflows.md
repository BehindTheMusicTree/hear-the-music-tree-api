# GitHub Actions Workflows

This document describes each GitHub Actions workflow in `.github/workflows/`.

## Table of Contents

- [Overview](#overview)
- [Test](#test)
  - [Debugging pytest hangs after django.setup()](#debugging-pytest-hangs-after-djangosetup)
- [Build and deploy](#build-and-deploy)
- [Static Files](#static-files)
- [Branch Protection](#branch-protection)
- [Labeler](#labeler)

## Overview

Tests, build and deployment, branch protection, release notes, and labeling use separate workflows.

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
   - `hear/test/conftest.py: imported` — confirms initial conftest import ran.
2. **Probe step:** The pytest job runs **`pytest --show-ini`** and **`pytest --trace-config`** (truncated) **before** the main `pytest` invocation so you can confirm **`inifile`**, **`rootdir`**, **`addopts`**, and registered plugins.
3. **Environment (set in `test.yml` for `docker compose run`):**
   - **`CI_STARTUP_TRACE=1`** — enables verbose `[Django]` / `[pytest]` diagnostics in application code.
   - **`PYTEST_PLUGINS=hear.ci_pytest_startup_plugin`** — loads the hook-bracket plugin even when a bind-mount hides image-local `*.egg-info` entry points.
   - **`PYTHONFAULTHANDLER=1`** — on hang, send **SIGQUIT** to the pytest process (e.g. from another shell: `docker kill -s QUIT <container>` or `kill -QUIT <pid>`) to dump Python stacks to stderr. A watchdog in `test.yml` does this automatically after 10 minutes so the dump lands in the job log even if nobody is watching the run live.
4. **Repo / image:** `pytest.ini` is **not** listed in `.dockerignore` so the Docker build context includes it; the workflow still bind-mounts the workspace for JUnit output.

For local reproduction with the same diagnostics: `CI_STARTUP_TRACE=1 PYTEST_PLUGINS=hear.ci_pytest_startup_plugin PYTHONFAULTHANDLER=1 docker compose exec api pytest hear/test/ …`

## Build and deploy

**File:** `.github/workflows/build-and-deploy.yml`

Builds the `runtime` image on a GitHub-hosted runner, pushes it to **GitHub Container Registry**, then triggers the Coolify deploy of **`htmt-api`** for the matching environment.

**Triggers:** **Push** to `develop` (staging) or `main` (production), or **workflow_dispatch** from either branch (e.g. to redeploy after a failed image pull). Runs are serialized per branch (workflow-level concurrency) so an older build can't overwrite a newer tag.

**Jobs:** **build** – checks **`APP_TITLE`** / **`API_DIR_NAME`** (`scripts/check-workflow-env.sh`), logs in to `ghcr.io` with **`GITHUB_TOKEN`** (`packages: write`), builds with GHA layer cache and pushes **`ghcr.io/behindthemusictree/htmt-api`** tagged **`staging`** (develop) or **`prod`** (main), plus **`sha-<short>`** always, with the commit SHA baked in as **`GIT_COMMIT`** (surfaced by `/health/`); **deploy-staging** / **deploy-prod** – `trigger-coolify-deploy` on Coolify app **`htmt-api`** (health check **`/health/`** against **`APP_ORIGIN_IP`**).

**Variables / secrets:** repo vars **`APP_TITLE`**, **`API_DIR_NAME`**; org vars **`COOLIFY_API_SUBDOMAIN`**, **`DOMAIN_NAME`**, **`DEPLOY_SSH_HOST`**, **`APP_ORIGIN_IP`**; org secret **`COOLIFY_API_TOKEN`**.

## Static Files

**File:** `.github/workflows/static-files.yml`

Collects Django static files and commits/pushes them back to the repo.

**Triggers:**

- **Callable** via `workflow_call` (used by Publish)

**Jobs:** **check-vars-and-secrets** (Check vars and secrets) – determines version from git tags and validates required env vars and secrets; **collect-and-push-static-files** (Static files) – Checkout → set up Python 3.14 → install deps → setup filesystem → `manage.py collectstatic --noinput` → git config → commit and push changes → output `collect_static_files_commit_hash` for downstream workflows.

**Environment:** `collect_static`. Outputs are used by Publish so Build uses the commit that includes collected static files and the correct version.

**Django `ENV`:** The workflow sets **`ENV=collect_static`** on the job (see `hear/settings.py`); it is **not** read from a GitHub Variable.

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
