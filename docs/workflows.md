# GitHub Actions Workflows

This document describes each GitHub Actions workflow in `.github/workflows/`.

## Table of Contents

- [Overview](#overview)
- [Test](#test)
- [Publish](#publish)
- [Build](#build)
- [Sync env to server](#sync-env-to-server)
- [Static Files](#static-files)
- [Branch Protection](#branch-protection)
- [Labeler](#labeler)

## Overview

Workflows are split by responsibility: tests run on every change; publishing runs on push to `main` or version tags (`v*`) via a single Publish workflow; branch protection and labeler run on pull requests. Reusable workflows (`test`, `build-and-push`, `static-files`) can be called by others or triggered manually. Workflows that use environment vars or secrets run a **check-vars-and-secrets** job first (script: `scripts/check-workflow-env.sh`); it fails if any required var or secret is missing.

**Versioning**: Application version is derived from git tags (e.g., `v0.3.4` → `0.3.4`). See [Versioning Strategy](versioning.md) for details.

## Test

**File:** `.github/workflows/test.yml`

Runs the full test suite with pytest.

**Triggers:**

- **Push** to `main`, `develop`, `release/*`, `hotfix/*`, `chore/*`
- **Pull request** targeting `main` or `develop`
- **Callable** by other workflows via `workflow_call` (optional `test_path` input)

**Jobs:** **pre-commit** – runs hooks via org [python-project-standards](https://github.com/BehindTheMusicTree/python-project-standards) [`reusable-pre-commit.yml` @ `v2.2.0`](https://github.com/BehindTheMusicTree/python-project-standards/blob/v2.2.0/.github/workflows/reusable-pre-commit.yml) (see [docs/ci/python-project-standards.md](ci/python-project-standards.md), [`STANDARDS_VERSION`](../STANDARDS_VERSION)); **check-vars-and-secrets** (Check vars and secrets) – validates required env vars and secrets; **pytest** (Pytest) – Checkout → set up Python 3.14 → install system deps → install pip deps → setup filesystem → run DB and AFP containers → wait for DB → copy fixtures → init Django data → run pytest → publish test results (JUnit XML).

**Environment:** `ci_test` (uses repo vars and secrets for DB, AFP, AcousticID, etc.).

**Versioning:** Always uses "test" as the version (tests don't require real version numbers).

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
4. **check-pinned-tags** – requires `DB_VERSION` and `AFP_VERSION` in Settings → Variables (no `latest`)
5. **set-version-api** / **set-version-db** / **set-version-afp** – shared workflows from `BehindTheMusicTree/github-workflows`
6. **redeploy-webhook-call** – shared workflow `call-redeployment-webhook`

**Environment:** **TEST** for main push and prerelease/dev tags (staging). **PROD** for release tags (production). DB and AFP image tags must be pinned in repo variables.

**Variables (org-level pool, same as Sync env):** `REDEPLOYMENT_ROOT` (e.g. `/var/webhook/redeployment`). Set once at the **organization** (Settings → Variables) so the infrastructure repo and all app repos that call set-image-tag-on-server use the same path. If unset, the tag file path is wrong and the step fails.

**Versioning:** Main push uses `VERSION` file and tag `staging`. Tag push uses tag version; `workflow_call` without a tag uses latest git tag.

**Migrations:** Not run by the workflow. The API container entrypoint runs `migrate` after the database is ready.

## Build And Push

**File:** `.github/workflows/build-and-push.yml`

Builds the app Docker image and pushes it to Docker Hub.

**Triggers:**

- **Callable** via `workflow_call` (optional `commit_hash`; optional `environment`, default `TEST`; used by Publish)

**Jobs:** **build-and-push-to-dockerhub** – checkout at ref → login to Docker Hub → build and push image with build-args from repo vars. Uses **environment** (TEST or PROD) for secrets/vars.

**Environment:** Dynamic from caller: **TEST** or **PROD**. Image tag: `$DOCKERHUB_USERNAME/$HTMT_API_IMAGE_REPO:$IMAGE_TAG`.

## Sync env to server

**File:** `.github/workflows/sync-env-to-server.yml`

Manually sync app env vars and secrets for **both STAGING and PROD** in one run. The shared workflow uploads the fragment to **`/tmp/sync-env-<HTMT_API_APP_NAME>-<env>.env`** on the VPS and merges into **`scripts/.env`**; **`generate-docker-compose.sh` requires that file** for secrets and API flags. **`FILE_UPLOAD_ENABLED`**, **`SPOTIFY_ENABLED`**, **`GOOGLE_OAUTH_ENABLED`**, **`MUSICBRAINZ_LOOKUP_ENABLED`**, and **`HTMT_API_AFP_ENABLED`** are **hardcoded `true`** in this workflow (no GitHub Variables). **Jobs:** **build-fragment** (matrix: STAGING and PROD), **sync-staging**, **sync-prod**. No `workflow_dispatch` inputs; one run syncs both environments.

**Triggers:** **workflow_dispatch** (Actions → Sync env to server → Run workflow). No inputs.

**Secrets (this repo, per environment):** `DB_APP_DB_NAME`, `DB_APP_USERNAME`, `DB_APP_USER_PASSWORD`, `DB_SUPERUSER_PASSWORD`, `DEMO_PASSWORD`, `DEMO_USERNAME`, `DJANGO_SECRET_KEY`, `GOOGLE_CLIENT_SECRET`, `SPOTIFY_CLIENT_SECRET`, `SUPERADMIN_PASSWORD`, `SUPERADMIN_USERNAME`, `TMTA_USERNAME`, plus deploy secrets `SERVER_DEPLOY_USERNAME`, `SERVER_DEPLOY_SSH_PRIVATE_KEY`.

**Variables (this repo or org, per GitHub Environment):** `VPS_IP`, `REDEPLOYMENT_ROOT`, `SYNC_ENV_REMOTE_FILENAME_PREFIX_BASE`, `HTMT_API_APP_NAME`, `DEMO_EMAIL`, `SUPERADMIN_EMAIL`, `SPOTIFY_CLIENT_ID_STAGING`, `SPOTIFY_CLIENT_ID_PROD`, `GOOGLE_CLIENT_ID_STAGING`, `GOOGLE_CLIENT_ID_PROD`, **`SPOTIFY_SCOPES`** (see `env/dev/.env.dev.example`). The compose-required API booleans above are **not** Variables—they are written as **`true`** in the workflow. Locally and in CI you still set **`FILE_UPLOAD_ENABLED`** in `env/.env` as needed (see `api/settings.py` / `TMP_UPLOADED_FILES`).

## Static Files

**File:** `.github/workflows/static-files.yml`

Collects Django static files and commits/pushes them back to the repo.

**Triggers:**

- **Callable** via `workflow_call` (used by Publish)

**Jobs:** **check-vars-and-secrets** (Check vars and secrets) – determines version from git tags and validates required env vars and secrets; **collect-and-push-static-files** (Static files) – Checkout → set up Python 3.14 → install deps → setup filesystem → `manage.py collectstatic --noinput` with version from job 1 → git config → commit and push changes → output `collect_static_files_commit_hash` and `app_version` for downstream workflows.

**Environment:** `collect_static`. Outputs are used by Publish so Build uses the commit that includes collected static files and the correct version.

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
