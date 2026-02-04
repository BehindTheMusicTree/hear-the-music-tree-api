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
  - Format: `v0.3.5-dev`
  - Example: `v0.3.5-dev` → Docker image: `username/repo:0.3.5-dev`

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

# Option 3: Create a development build
git tag v0.3.5-dev
git push origin v0.3.5-dev
# Automatically builds and deploys: username/repo:0.3.5-dev
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
