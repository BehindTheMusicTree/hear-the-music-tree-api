# GitHub Actions Workflows

This document describes each GitHub Actions workflow in `.github/workflows/`.

## Table of Contents

- [Overview](#overview)
- [Test](#test)
- [Publish](#publish)
- [Build](#build)
- [Deploy](#deploy)
- [Static Files](#static-files)
- [Branch Protection](#branch-protection)
- [Labeler](#labeler)

## Overview

Workflows are split by responsibility: tests run on every change; publishing (static files, build, deploy) runs on version tags; branch protection and labeler run on pull requests. Reusable workflows (`test`, `build`, `static-files`, `deploy`) can be called by others or triggered manually.

## Test

**File:** `.github/workflows/test.yml`

Runs the full test suite with pytest.

**Triggers:**

- **Push** to `main`, `develop`, `release/*`, `hotfix/*`, `chore/*`
- **Pull request** targeting `main` or `develop`
- **Manual** via `workflow_dispatch` (optional `test_path` input)
- **Callable** by other workflows via `workflow_call` (optional `test_path` input)

**Steps:** Checkout → setup Python 3.14 → install system deps → install pip deps → setup filesystem → run DB and AFP containers → wait for DB → copy fixtures → init Django data → run pytest → publish test results (JUnit XML).

**Environment:** `CI_TEST` (uses repo vars and secrets for DB, AFP, AcousticID, etc.).

## Publish

**File:** `.github/workflows/publish.yml`

Orchestrates release: collect static files, build Docker image, deploy to the test server.

**Triggers:**

- **Push** of version tags (`v*`, e.g. `v0.2.1`)
- **Manual** via `workflow_dispatch`
- **Callable** by other workflows via `workflow_call`

**Jobs (sequential):**

1. **static** – calls `static-files.yml`, commits and pushes collected static files
2. **build** – calls `build.yml` with the commit hash from step 1
3. **deploy** – calls `deploy.yml` to deploy to the test server

**Environment:** Uses `TEST` environment vars and secrets.

## Build

**File:** `.github/workflows/build.yml`

Builds the app Docker image and pushes it to Docker Hub.

**Triggers:**

- **Manual** via `workflow_dispatch` (optional `commit_hash` input)
- **Callable** via `workflow_call` (optional `commit_hash` input; used by Publish)

**Steps:** Checkout (at given ref) → login to Docker Hub → build and push image with build-args from repo vars.

**Environment:** `TEST`. Image tag: `$DOCKERHUB_USERNAME/$APP_IMAGE_REPO:$APP_VERSION`.

## Deploy

**File:** `.github/workflows/deploy.yml`

Deploys the application to the test server via SSH and redeployment webhook.

**Triggers:**

- **Manual** via `workflow_dispatch`
- **Callable** via `workflow_call` (used by Publish)

**Jobs:**

1. **set-env-variables-on-server** – SSH to server, write API, DB, and AFP `.env` files from GitHub vars/secrets
2. **set-partial-docker-compose-on-server** – generate partial Docker Compose files with `generate-docker-compose-parts.sh`, SCP them to the server
3. **redeploy-webhook-call** – call Bodzify server-management redeployment webhook (depends on jobs 1 and 2)

**Environment:** `TEST`. Uses `TEST_SERVER_SSH_BODZIFY_PRIVATE_KEY`, `DOMAIN_NAME`, `WEBHOOK_DIR`, etc.

## Static Files

**File:** `.github/workflows/static-files.yml`

Collects Django static files and commits/pushes them back to the repo.

**Triggers:**

- **Manual** via `workflow_dispatch`
- **Callable** via `workflow_call` (used by Publish)

**Steps:** Checkout → setup Python 3.14 → install deps → setup filesystem → `manage.py collectstatic --noinput` → git config → commit and push changes → output `collect_static_files_commit_hash` for downstream workflows.

**Environment:** `COLLECT_STATIC`. Output is used by Publish so Build uses the commit that includes collected static files.

## Branch Protection

**File:** `.github/workflows/branch-protection.yml`

Enforces Git Flow: only allows certain source branches for PRs to `main` and `develop`.

**Triggers:**

- **Pull request** targeting `main` or `develop`

**Logic:**

- **PRs to `main`:** source branch must be `hotfix/*` or `release/*`; otherwise the job fails
- **PRs to `develop`:** source branch must be `feature/*`, `chore/*`, `dependabot/*`, or `release/*`; otherwise the job fails

**No manual or workflow_call;** runs only on PR open/sync.

## Labeler

**File:** `.github/workflows/labeler.yml`

Adds labels to pull requests based on changed files using `.github/labeler.yml`.

**Triggers:**

- **Pull request** events: `opened`, `synchronize`, `reopened`, `labeled`, `unlabeled`

**Steps:** Checkout (full depth) → run `actions/labeler@v5` with `sync-labels: true`.

**Permissions:** `contents: read`, `pull-requests: write`.
