# GitHub Actions Workflows

This document describes each GitHub Actions workflow in `.github/workflows/`.

## Table of Contents

- [Overview](#overview)
- [Test](#test)
- [Publish](#publish)
- [Build](#build)
- [Deploy](#deploy)
- [Sync env to server](#sync-env-to-server)
- [Static Files](#static-files)
- [Branch Protection](#branch-protection)
- [Labeler](#labeler)

## Overview

Workflows are split by responsibility: tests run on every change; publishing (static files, build, deploy) runs on version tags; branch protection and labeler run on pull requests. Reusable workflows (`test`, `build`, `static-files`, `deploy`) can be called by others or triggered manually. Workflows that use environment vars or secrets run a **check-vars-and-secrets** job first (script: `scripts/check-workflow-env.sh`); it fails if any required var or secret is missing.

**Versioning**: Application version is derived from git tags (e.g., `v0.3.4` → `0.3.4`). See [Versioning Strategy](versioning.md) for details.

## Test

**File:** `.github/workflows/test.yml`

Runs the full test suite with pytest.

**Triggers:**

- **Push** to `main`, `develop`, `release/*`, `hotfix/*`, `chore/*`
- **Pull request** targeting `main` or `develop`
- **Callable** by other workflows via `workflow_call` (optional `test_path` input)

**Jobs:** **check-vars-and-secrets** (Check vars and secrets) – validates required env vars and secrets; **pytest** (Pytest) – Checkout → set up Python 3.14 → install system deps → install pip deps → setup filesystem → run DB and AFP containers → wait for DB → copy fixtures → init Django data → run pytest → publish test results (JUnit XML).

**Environment:** `ci_test` (uses repo vars and secrets for DB, AFP, AcousticID, etc.).

**Versioning:** Always uses "test" as the version (tests don't require real version numbers).

## Publish

**File:** `.github/workflows/publish.yml`

Orchestrates release: collect static files, build Docker image, deploy to the test server.

**Triggers:**

- **Push** of version tags (`v*`, e.g. `v0.2.1`)
- **Callable** by other workflows via `workflow_call`

**Jobs (sequential):**

1. **determine-version** (Determine version) – extracts version from git tag
2. **static** (Static files) – calls `static-files.yml`, commits and pushes collected static files
3. **build-and-push** (Docker image) – calls `build-and-push.yml` with commit hash from step 2
4. **deploy** (Deploy) – calls `deploy.yml` to deploy to the test server

**Environment:** Uses `TEST` environment vars and secrets. **DB and AFP image tags must be pinned:** set `DB_IMAGE_VERSION` and `AFP_IMAGE_VERSION` (e.g. `16`, `1.0`) in Settings → Variables; the workflow fails if they are unset (no `latest`).

**Versioning:** Version is automatically extracted from git tags (e.g., `refs/tags/v0.3.4` → `0.3.4`). If not triggered by a tag, it fetches the latest git tag.

## Build And Push

**File:** `.github/workflows/build-and-push.yml`

Builds the app Docker image and pushes it to Docker Hub.

**Triggers:**

- **Callable** via `workflow_call` (optional `commit_hash` input; used by Publish)

**Jobs:** **check-vars-and-secrets** (Check vars and secrets) – determines version from git tags and validates required env vars and secrets; **build-and-push-to-dockerhub** (Push to Docker Hub) – checkout at ref → login to Docker Hub → build and push image with build-args from repo vars.

**Environment:** `TEST`. Image tag: `$DOCKERHUB_USERNAME/$HTMT_API_IMAGE_REPO:$APP_VERSION` (version determined from git tags).

## Deploy

**File:** `.github/workflows/deploy.yml`

Deploys the application to the test server via SSH and redeployment webhook.

**Triggers:**

- **Callable** via `workflow_call` (used by Publish)

**Jobs:**

1. **check-vars-and-secrets** (Check vars and secrets) – determines version from git tags and validates required env vars and secrets
2. **set-env-variables-on-server** (Set env vars) – SSH to server, write API, DB, and AFP `.env` files from GitHub vars/secrets
3. **set-partial-docker-compose-on-server** (Set compose files) – generate partial Docker Compose files with `generate-docker-compose-parts.sh` using version from job 1, SCP them to the server
4. **redeploy-webhook-call** (Redeploy webhook) – call BehindTheMusicTree server-management redeployment webhook (depends on jobs 2 and 3)

**Environment:** `TEST`. Uses `SERVER_DEPLOY_SSH_PRIVATE_KEY`, `DOMAIN_NAME`, `WEBHOOK_DIR`, etc.

**Migrations:** The workflow does not run Django migrations. Migrations are applied when the container starts: the API container entrypoint (`scripts/entrypoint.sh`) runs `migrate` after the database is ready, so each new deployment applies pending migrations before Gunicorn starts.

## Sync env to server

**File:** `.github/workflows/sync-env-to-server.yml`

Manually sync app env vars and secrets to the server `scripts/.env` (test and prod). Only the listed keys are updated; other keys in `.env` (set by the infrastructure repo) are unchanged.

**Triggers:** **workflow_dispatch** (Actions → Sync env to server → Run workflow).

**Secrets (this repo):** `DB_APP_DB_NAME`, `DB_APP_USERNAME`, `DB_APP_USER_PASSWORD`, `DB_SUPERUSER_PASSWORD`, `DEMO_PASSWORD`, `DEMO_USERNAME`, `DJANGO_SECRET_KEY`, `GOOGLE_CLIENT_SECRET`, `SPOTIFY_CLIENT_SECRET`, `SUPERADMIN_PASSWORD`, `SUPERADMIN_USERNAME`, `TMTA_USERNAME`, plus deploy secrets `SERVER_DEPLOY_USERNAME`, `SERVER_DEPLOY_SSH_PRIVATE_KEY`.

**Variables (this repo):** `DEMO_EMAIL`, `SUPERADMIN_EMAIL`, `FILE_UPLOAD_ENABLED`, and deploy vars `DOMAIN_NAME`, `WEBHOOK_DIR`, `WEBHOOK_REDEPLOYMENT_DIR_NAME_BASE`.

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

**Jobs:** **check-branch-name** (Verify PR source branch) – validates source branch against target per Git Flow.

**Logic:**

- **PRs to `main`:** source branch must be `hotfix/*` or `release/*`; otherwise the job fails
- **PRs to `develop`:** source branch must be `feature/*`, `chore/*`, `dependabot/*`, or `release/*`; otherwise the job fails

**No manual or workflow_call;** runs only on PR open/sync.

## Labeler

**File:** `.github/workflows/labeler.yml`

Adds labels to pull requests based on changed files using `.github/labeler.yml`.

**Triggers:**

- **Pull request** events: `opened`, `synchronize`, `reopened`, `labeled`, `unlabeled`

**Jobs:** **label** (Auto Label PR) – Checkout (full depth) → run `actions/labeler@v5` with `sync-labels: true`.

**Permissions:** `contents: read`, `pull-requests: write`.
