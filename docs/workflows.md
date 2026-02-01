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

Workflows are split by responsibility: tests run on every change; publishing (static files, build, deploy) runs on version tags; branch protection and labeler run on pull requests. Reusable workflows (`test`, `build`, `static-files`, `deploy`) can be called by others or triggered manually. Workflows that use environment vars or secrets run a **check-vars-and-secrets** job first (script: `scripts/check-workflow-env.sh`); it fails if any required var or secret is missing.

## Test

**File:** `.github/workflows/test.yml`

Runs the full test suite with pytest.

**Triggers:**

- **Push** to `main`, `develop`, `release/*`, `hotfix/*`, `chore/*`
- **Pull request** targeting `main` or `develop`
- **Manual** via `workflow_dispatch` (optional `test_path` input)
- **Callable** by other workflows via `workflow_call` (optional `test_path` input)

**Jobs:** **check-vars-and-secrets** (Check vars and secrets) – validates required env vars and secrets; **pytest** (Pytest) – Checkout → set up Python 3.14 → install system deps → install pip deps → setup filesystem → run DB and AFP containers → wait for DB → copy fixtures → init Django data → run pytest → publish test results (JUnit XML).

**Environment:** `CI_TEST` (uses repo vars and secrets for DB, AFP, AcousticID, etc.).

## Publish

**File:** `.github/workflows/publish.yml`

Orchestrates release: collect static files, build Docker image, deploy to the test server.

**Triggers:**

- **Push** of version tags (`v*`, e.g. `v0.2.1`)
- **Manual** via `workflow_dispatch`
- **Callable** by other workflows via `workflow_call`

**Jobs (sequential):**

1. **static** (Static files) – calls `static-files.yml`, commits and pushes collected static files
2. **build** (Docker image) – calls `build.yml` with the commit hash from step 1
3. **deploy** (Deploy) – calls `deploy.yml` to deploy to the test server

**Environment:** Uses `TEST` environment vars and secrets.

## Build

**File:** `.github/workflows/build.yml`

Builds the app Docker image and pushes it to Docker Hub.

**Triggers:**

- **Manual** via `workflow_dispatch` (optional `commit_hash` input)
- **Callable** via `workflow_call` (optional `commit_hash` input; used by Publish)

**Jobs:** **check-vars-and-secrets** (Check vars and secrets) – validates required env vars and secrets; **build-and-push-to-dockerhub** (Push to Docker Hub) – checkout at ref → login to Docker Hub → build and push image with build-args from repo vars.

**Environment:** `TEST`. Image tag: `$DOCKERHUB_USERNAME/$APP_IMAGE_REPO:$APP_VERSION`.

## Deploy

**File:** `.github/workflows/deploy.yml`

Deploys the application to the test server via SSH and redeployment webhook.

**Triggers:**

- **Manual** via `workflow_dispatch`
- **Callable** via `workflow_call` (used by Publish)

**Jobs:**

1. **check-vars-and-secrets** (Check vars and secrets) – validates required env vars and secrets
2. **set-env-variables-on-server** (Set env vars) – SSH to server, write API, DB, and AFP `.env` files from GitHub vars/secrets
3. **set-partial-docker-compose-on-server** (Set compose files) – generate partial Docker Compose files with `generate-docker-compose-parts.sh`, SCP them to the server
4. **redeploy-webhook-call** (Redeploy webhook) – call BehindTheMusicTree server-management redeployment webhook (depends on jobs 2 and 3)

**Environment:** `TEST`. Uses `SERVER_DEPLOY_SSH_PRIVATE_KEY`, `DOMAIN_NAME`, `WEBHOOK_DIR`, etc.

## Static Files

**File:** `.github/workflows/static-files.yml`

Collects Django static files and commits/pushes them back to the repo.

**Triggers:**

- **Manual** via `workflow_dispatch`
- **Callable** via `workflow_call` (used by Publish)

**Jobs:** **check-vars-and-secrets** (Check vars and secrets) – validates required env vars and secrets; **collect-and-push-static-files** (Static files) – Checkout → set up Python 3.14 → install deps → setup filesystem → `manage.py collectstatic --noinput` → git config → commit and push changes → output `collect_static_files_commit_hash` for downstream workflows.

**Environment:** `COLLECT_STATIC`. Output is used by Publish so Build uses the commit that includes collected static files.

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
