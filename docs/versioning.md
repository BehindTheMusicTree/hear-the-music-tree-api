# Versioning Strategy

This document describes how application versioning is handled in CI/CD workflows.

## Table of Contents

- [Overview](#overview)
- [Version Format](#version-format)
- [API URL path prefix](#api-url-path-prefix)
- [Pre-Release Versions](#pre-release-versions)
  - [Development Tags (`-dev`)](#development-tags--dev-)
  - [Release Candidate Tags (`-rc`, `-beta`, `-alpha`)](#release-candidate-tags--rc--beta--alpha-)
- [How Versioning Works](#how-versioning-works)
  - [Release Workflow (`publish.yml`)](#release-workflow-publishyml)
  - [Version Extraction Logic](#version-extraction-logic)
- [Benefits](#benefits)
- [Usage Examples](#usage-examples)
  - [Creating a Release](#creating-a-release)
  - [Development Version Tag Testing](#development-version-tag-testing)
  - [Pre-Release Version Tag Testing](#pre-release-version-tag-testing)
- [Workflows Using Versioning](#workflows-using-versioning)

## Overview

The application version is derived from **git tags**. Git tags (e.g., `v0.2.0`) serve as the single source of truth for versioning. The workflow extracts the version number (e.g., `0.2.0`) from the tag name.

## Version Format

Versions follow semantic versioning with a `v` prefix:

- Format: `v<major>.<minor>.<patch>` (e.g., `v0.2.0`)
- The `v` prefix is stripped when used in workflows (e.g., `v0.2.0` → `0.2.0`)

## API URL path prefix

The API URL path prefix uses the **major version only** (e.g. `v1/`). It is derived from `APP_VERSION` at runtime: for `APP_VERSION=1.2.3`, the prefix is `v1/`. This keeps client URLs stable across minor and patch releases; only a new major version would change the path prefix.

## Pre-Release Versions

Pre-release version tags are used to test builds and deployments on the test server before final release. They follow semantic versioning conventions and are supported by the workflow system. All pre-release version tags automatically trigger the `publish.yml` workflow, which builds the application, creates a Docker image, and deploys it to the test server.

There are two main categories of pre-release versions, distinguished by **when** they're used and **where** they're created:

### Development Tags (`-dev`)

Development version tags are used to test builds and deployments from **feature and hotfix branches** during active development, before merging to `develop` or creating a release branch.

#### Format

- Format: `v<version>-dev-<branch-name>` (e.g., `v0.3.6-dev-improve-cicd`)
- Use the branch name **without** the type prefix (`feature/`, `hotfix/`, etc.)
- Example: Branch `feature/improve-cicd` → Tag `v0.3.6-dev-improve-cicd` → Docker image: `username/repo:0.3.6-dev-improve-cicd`

#### Naming Convention

Development version tags should include the branch name (without type prefix) to identify what's being tested:

- **Feature branches**: `feature/improve-cicd` → `v0.3.6-dev-improve-cicd`
- **Hotfix branches**: `hotfix/critical-bug` → `v0.3.6-dev-critical-bug`

#### Version Selection

Since the actual release version isn't known until the release branch is created, use these guidelines:

- **Feature branches**: Typically minor version updates (e.g., `v0.3.6-dev-*` or `v0.4.0-dev-*`)
- **Hotfix branches**: Typically patch version updates (e.g., `v0.3.6-dev-*`)
- **Breaking changes**: Major version (e.g., `v1.0.0-dev-*`)

The version number is a placeholder - the actual release version is determined when creating the release branch.

#### Workflow Behavior

When you push a development version tag (e.g., `v0.3.6-dev-improve-cicd`), the workflow automatically:

1. **Extracts the version number** from the tag: `v0.3.6-dev-improve-cicd` → `0.3.6-dev-improve-cicd`
2. **Collects static files** and commits them (via `static-files.yml`)
3. **Builds Docker image** with that version: `username/repo:0.3.6-dev-improve-cicd`
4. **Sets image tags on server** (API, DB, AFP) and **triggers redeploy webhook** to deploy to the test server

#### Republishing Development Version Tags

Git tags are immutable once pushed. If you need to republish after making changes:

1. **Delete and recreate** (recommended for development version tags):

   ```bash
   git tag -d v0.3.6-dev-improve-cicd
   git push origin --delete v0.3.6-dev-improve-cicd
   git tag v0.3.6-dev-improve-cicd
   git push origin v0.3.6-dev-improve-cicd
   ```

2. **Or use incrementing suffix** (if you want to keep history):
   ```bash
   git tag v0.3.6-dev-improve-cicd-1  # First iteration
   git push origin v0.3.6-dev-improve-cicd-1
   # After changes:
   git tag v0.3.6-dev-improve-cicd-2  # Second iteration
   git push origin v0.3.6-dev-improve-cicd-2
   ```

### Release Candidate Tags (`-rc`, `-beta`, `-alpha`)

Release candidate version tags are used to test builds and deployments from **release branches** before final release. These are created during the release process when features are complete and ready for final testing.

#### Pre-Release Identifiers

- **`rc`** (Release Candidate): A version that is feature-complete and ready for final testing before release. **RC** stands for "Release Candidate" - it's a candidate for becoming the final release if testing passes.

  - Format: `v0.2.0-rc1`, `v0.2.0-rc2`, etc.
  - Example: `v0.2.0-rc1` → Docker image: `username/repo:0.2.0-rc1`

- **`beta`** (Beta Release): An early release for testing with most features complete but may have known issues.

  - Format: `v0.2.0-beta1`, `v0.2.0-beta2`, etc.
  - Example: `v0.2.0-beta1` → Docker image: `username/repo:0.2.0-beta1`

- **`alpha`** (Alpha Release): An early development release for internal testing.
  - Format: `v0.2.0-alpha1`, `v0.2.0-alpha2`, etc.
  - Example: `v0.2.0-alpha1` → Docker image: `username/repo:0.2.0-alpha1`

#### Workflow Behavior

When you push a release candidate version tag (e.g., `v0.2.0-rc1`), the workflow automatically:

1. **Extracts the version number** from the tag: `v0.2.0-rc1` → `0.2.0-rc1`
2. **Collects static files** and commits them (via `static-files.yml`)
3. **Builds Docker image** with that version: `username/repo:0.2.0-rc1`
4. **Sets image tags on server** (API, DB, AFP) and **triggers redeploy webhook** to deploy to the test server

### Cleanup

All pre-release version tags (dev, rc, beta, alpha) should be deleted during the release process to keep the repository clean. See [Creating a Release](#creating-a-release) for cleanup steps.

## How Versioning Works

### Release Workflow (`publish.yml`)

Single publish workflow, triggered by:

- **Push to `main`**: Uses `VERSION` file, image tag `staging`, deploys to staging (TEST env).
- **Push of version tag** (e.g. `git push origin v0.2.0`): Extracts version from the tag; prerelease (tag contains `-`) → TEST/staging; release → PROD/production.

The workflow extracts the version from the ref, uses it for the Docker image tag and server image tag, then triggers the redeployment webhook.

## Benefits

1. **Single source of truth**: Version number is tied to git history via git tags
2. **No manual updates**: Version number is automatically derived from git tags
3. **Traceability**: Version number is directly linked to the git commit/tag
4. **Industry standard**: Follows common CI/CD best practices
5. **DRY principle**: Version number is extracted once from the git tag and used consistently

## Usage Examples

### Creating a Release

**Source of truth:** full Git Flow (release branch, `python3 scripts/prepare_release_bump.py` or `bump-my-version bump …` by hand, `CHANGELOG.md`, PR to `main`, tag with `v` prefix, merge back to `develop`, delete release branch) is documented in [CONTRIBUTING.md](../CONTRIBUTING.md#7-releasing-for-maintainers) §7. The steps below are a short tag/publish reminder only.

```bash
# After VERSION and CHANGELOG on main match the release (see CONTRIBUTING.md §7):

# 1. Tag and push (triggers publish.yml when CI allows)
git tag v0.2.0
git push origin v0.2.0

# 2. Clean up pre-release version tags (dev, rc, beta, alpha) for that version, or use:
#    ./scripts/remove_prerelease_tags.sh
```

### Development Version Tag Testing

For testing builds and deployments from feature or hotfix branches:

```bash
# On a feature branch
git checkout feature/improve-cicd
git tag v0.3.6-dev-improve-cicd
git push origin v0.3.6-dev-improve-cicd
# Automatically builds and deploys: username/repo:0.3.6-dev-improve-cicd
```

### Pre-Release Version Tag Testing

For testing builds and deployments on the test server before final release:

```bash
# Option 1: Create a release candidate version tag (recommended)
git tag v0.2.0-rc1
git push origin v0.2.0-rc1
# Automatically builds and deploys: username/repo:0.2.0-rc1

# Option 2: Create a beta version tag
git tag v0.2.0-beta1
git push origin v0.2.0-beta1
# Automatically builds and deploys: username/repo:0.2.0-beta1

# Option 3: Create an alpha version tag
git tag v0.2.0-alpha1
git push origin v0.2.0-alpha1
# Automatically builds and deploys: username/repo:0.2.0-alpha1
```
