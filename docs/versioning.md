# Versioning Strategy

This document describes how application versioning is handled in CI/CD workflows.

## Table of Contents

- [Overview](#overview)
- [Version Format](#version-format)
- [Pre-Release Versions](#pre-release-versions)
- [How Versioning Works](#how-versioning-works)
  - [Release Workflow (`publish.yml`)](#release-workflow-publishyml)
  - [Version Extraction Logic](#version-extraction-logic)
- [Benefits](#benefits)
- [Usage Examples](#usage-examples)
  - [Creating a Release](#creating-a-release)
  - [Pre-Release Testing](#pre-release-testing)
- [Workflows Using Versioning](#workflows-using-versioning)
- [Backward Compatibility](#backward-compatibility)

## Overview

The application version is derived from **git tags**. This follows industry best practices by using git tags as the single source of truth for versioning.

## Version Format

Versions follow semantic versioning with a `v` prefix:
- Format: `v<major>.<minor>.<patch>` (e.g., `v0.3.4`)
- The `v` prefix is stripped when used in workflows (e.g., `v0.3.4` → `0.3.4`)

## Pre-Release Versions

For testing Docker images on the test server before final release, you can use pre-release version identifiers. These follow semantic versioning conventions and are supported by the workflow system.

### Pre-Release Identifiers

- **`rc`** (Release Candidate): A version that is feature-complete and ready for final testing before release. **RC** stands for "Release Candidate" - it's a candidate for becoming the final release if testing passes.
  - Format: `v0.3.5-rc1`, `v0.3.5-rc2`, etc.
  - Example: `v0.3.5-rc1` → Docker image: `username/repo:0.3.5-rc1`

- **`beta`** (Beta Release): An early release for testing with most features complete but may have known issues.
  - Format: `v0.3.5-beta1`, `v0.3.5-beta2`, etc.
  - Example: `v0.3.5-beta1` → Docker image: `username/repo:0.3.5-beta1`

- **`alpha`** (Alpha Release): An early development release for internal testing.
  - Format: `v0.3.5-alpha1`, `v0.3.5-alpha2`, etc.
  - Example: `v0.3.5-alpha1` → Docker image: `username/repo:0.3.5-alpha1`

- **`dev`** (Development Build): A development build, typically used for feature branch testing.
  - Format: `v0.3.6-dev-<branch-name>` (e.g., `v0.3.6-dev-improve-cicd`)
  - Use branch name **without** the type prefix (`feature/`, `hotfix/`, etc.)
  - Example: Branch `feature/improve-cicd` → Tag `v0.3.6-dev-improve-cicd` → Docker image: `username/repo:0.3.6-dev-improve-cicd`

### Dev Tag Naming Convention

Dev tags should include the branch name (without type prefix) to identify what's being tested:

- **Feature branches**: `feature/improve-cicd` → `v0.3.6-dev-improve-cicd`
- **Hotfix branches**: `hotfix/critical-bug` → `v0.3.6-dev-critical-bug`

**Version Selection:**

Since the actual release version isn't known until the release branch is created, use these guidelines:

- **Feature branches**: Typically minor version updates (e.g., `v0.3.6-dev-*` or `v0.4.0-dev-*`)
- **Hotfix branches**: Typically patch version updates (e.g., `v0.3.6-dev-*`)
- **Breaking changes**: Major version (e.g., `v1.0.0-dev-*`)

The version number is a placeholder - the actual release version is determined when creating the release branch.

**Republishing Dev Tags:**

Git tags are immutable once pushed. If you need to republish after making changes:

1. **Delete and recreate** (recommended for dev tags):
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

**Cleanup:**

All pre-release tags (dev, rc, beta, alpha) should be deleted during the release process to keep the repository clean. See [Creating a Release](#creating-a-release) for cleanup steps.

### Usage for Testing

Pre-release versions are particularly useful for:

1. **Testing on test server**: Build and deploy Docker images with pre-release tags to validate functionality before final release
2. **Release candidates**: Use `-rc1`, `-rc2`, etc. for versions that are ready for final testing
3. **Feature testing**: Use `-dev` or `-beta` for testing new features before they're ready for release

When you push a pre-release tag (e.g., `v0.3.5-rc1`), the workflow automatically:
- Extracts the version: `v0.3.5-rc1` → `0.3.5-rc1`
- Builds Docker image: `username/repo:0.3.5-rc1`
- Deploys to test server with that version

## How Versioning Works

### Release Workflow (`publish.yml`)

When a version tag is pushed (e.g., `git push origin v0.3.4`), the `publish.yml` workflow:

1. **Extracts version from tag**: The workflow automatically extracts the version from `github.ref` (e.g., `refs/tags/v0.3.4` → `0.3.4`)

2. **Passes version to child workflows**: The extracted version is passed as an input to reusable workflows:
   - `static-files.yml` - for collecting static files
   - `build.yml` - for building Docker images
   - `deploy.yml` - for deployment

3. **Uses version throughout pipeline**:
   - Docker image tags: `username/repo:0.3.4`
   - Django API URL paths: `api/0.3.4/`
   - Docker Compose service configurations

### Version Extraction Logic

The version is determined using the following priority:

1. **From tag ref** (when triggered by tag push):
   ```yaml
   # github.ref = refs/tags/v0.3.4
   VERSION="${GITHUB_REF#refs/tags/v}"  # Result: 0.3.4
   ```
   Works with pre-release tags too: `refs/tags/v0.3.5-rc1` → `0.3.5-rc1`

2. **From latest git tag** (fallback when not triggered by tag):
   ```bash
   git fetch --tags --force
   LATEST_TAG=$(git describe --tags --abbrev=0)
   VERSION="${LATEST_TAG#v}"  # Remove 'v' prefix
   ```

## Benefits

1. **Single source of truth**: Version is tied to git history
2. **No manual updates**: Version is automatically derived from git tags
3. **Traceability**: Version is directly linked to the git commit/tag
4. **Industry standard**: Follows common CI/CD best practices
5. **DRY principle**: Version is extracted once and passed to child workflows

## Usage Examples

### Creating a Release

```bash
# 1. Create release branch
git checkout -b release/v0.3.4

# 2. Merge to main
git checkout main
git merge release/v0.3.4

# 3. Tag the release
git tag v0.3.4
git push origin v0.3.4  # Triggers publish.yml workflow

# 4. Clean up pre-release tags (dev, rc, beta, alpha)
git tag -l "v0.3.4-dev-*" "v0.3.4-rc*" "v0.3.4-beta*" "v0.3.4-alpha*" | xargs -n 1 git tag -d
git tag -l "v0.3.4-dev-*" "v0.3.4-rc*" "v0.3.4-beta*" "v0.3.4-alpha*" | xargs -n 1 git push origin --delete
```

### Pre-Release Testing

For testing Docker images on the test server before final release:

```bash
# Option 1: Create a release candidate tag (recommended)
git tag v0.3.5-rc1
git push origin v0.3.5-rc1
# Automatically builds and deploys: username/repo:0.3.5-rc1

# Option 2: Create a beta release
git tag v0.3.5-beta1
git push origin v0.3.5-beta1
# Automatically builds and deploys: username/repo:0.3.5-beta1

# Option 3: Create a development build for feature branch testing
git tag v0.3.6-dev-improve-cicd  # branch: feature/improve-cicd
git push origin v0.3.6-dev-improve-cicd
# Automatically builds and deploys: username/repo:0.3.6-dev-improve-cicd
# Static files are committed to the feature branch
```

All pre-release tags automatically trigger the `publish.yml` workflow, which builds the Docker image and deploys it to the test server.

## Workflows Using Versioning

- **publish.yml**: Extracts version and orchestrates release
- **static-files.yml**: Uses version for Django static file collection
- **build.yml**: Uses version for Docker image tagging
- **deploy.yml**: Uses version for Docker Compose configuration
- **test.yml**: Uses version for test environment (falls back to latest git tag if available)

## Backward Compatibility

For workflows that may run outside of tag contexts (e.g., `test.yml` on PRs), the workflow will attempt to fetch the latest git tag. If no tags are available, workflows may use a default test version.
