# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## Changelog Best Practices

### General Principles

- Changelogs are for humans, not machines.
- Include an entry for every version, with the latest first.
- Group similar changes under: Added, Changed, Improved, Deprecated, Removed, Fixed, Documentation, Performance, CI.
- **"Test" is NOT a valid changelog category** - tests should be mentioned within the related feature or fix entry, not as standalone entries.
- Use an "Unreleased" section for upcoming changes.
- Follow Semantic Versioning where possible.
- Use ISO 8601 date format: YYYY-MM-DD.
- Avoid dumping raw git logs; summarize notable changes clearly.

### Guidelines for Contributors

All contributors (including maintainers) should update `CHANGELOG.md` when creating PRs:

1. **Add entries to the `[Unreleased]` section** - Add your changes under the appropriate category (Added, Changed, Improved, Deprecated, Removed, Fixed, Documentation, Performance, CI)
2. **Follow the changelog format** - See examples below and `.cursor/rules/changelog-best-practices.mdc` for detailed guidelines
3. **Group related changes** - Similar changes should be grouped together
4. **Be descriptive** - Write clear, user-focused descriptions of what changed
5. **Mention tests when relevant** - Tests should be mentioned within the related feature or fix entry, not as standalone entries

**Example:**

```markdown
## [Unreleased]

### Added

- **Track API**: Added batch upload endpoint for multiple tracks
  - Includes comprehensive unit tests covering various file formats and error scenarios
  - Supports parallel upload processing for improved performance

- **Genre Hierarchy**: Added support for custom genre tree import via JSON
  - Includes validation tests for tree structure and circular reference detection

### Fixed

- **Track Upload**: Fixed issue with handling large audio files exceeding size limits
  - Includes regression tests to prevent future occurrences
  - Improved error messages for better user feedback

### CI

- **Branch Protection**: Added automated enforcement of Git Flow branching rules
  - Blocks invalid PRs to main and develop branches
```

**Note:** During releases, maintainers will move entries from `[Unreleased]` to a versioned section (e.g., `## [0.2.8] - 2025-01-XX`).

## [Unreleased]

### Fixed

- **Spotify**: Added SpotifyAuthenticationException to custom exception handler for improved error handling

### Improved

- **env**: Add SUPERADMIN and DEMO credentials to .env.dev.example for enhanced configuration

## [v1.0.4] - 2026-02-13

### Added

-  **Users**: Added SUPERADMIN and DEMO environment variables to deployment workflow for enhanced configuration

## [v1.0.3] - 2026-02-13

### Changed

- **Dependencies**: Upgrade drf-spectacular to version 0.29.0

- **OpenAPI schema**: Title and version now configurable and aligned with app
  - OpenAPI `info.version` uses `APP_VERSION` (e.g. 1.0.4) instead of hardcoded 0.1.0
  - OpenAPI title set via `APP_TITLE` for human-readable docs title

- **OpenAPI schema**: Path prefix updated for subdomain deployment
  - `SCHEMA_PATH_PREFIX` changed from `/api/v[0-9]` to `/v[\d.]+` so it matches the version segment only (no `/api/` prefix)

### Fixed

- **OpenAPI schema**: Fix TypeError when generating schema for models with DecimalField/GeneratedField
  - Add custom AppAutoSchema that maps GeneratedField via output_field and passes max_digits/decimal_places for DecimalField so /schema/ and docs endpoints work

## [v1.0.2] - 2026-02-13

### Added

- **Reference Contexts**: Implement public read-only reference contexts for all major API endpoints
  - Add reference contexts for genres, albums, artists, plays, tags, and library/uploaded endpoints
  - Create Reference ViewSets with AllowAny permissions and system user fallback for public access
  - Add ReferencePlaylistViewSet and ReferenceManualPlaylistViewSet so reference/playlists and reference/manual-playlists expose system-owned public data
  - Restructure URL paths to hierarchical design (/me/ and /reference/ scopes)
  - Update router registrations in urls.py for new hierarchical paths
  - Regenerate API documentation with contexts tables for all endpoints
  - Update test reverse calls and import paths to reflect new URL structure
  - Modify Bruno test files to use new hierarchical URLs
  - Ensure all endpoint tests pass with the new reference contexts

- **Health Check**: Add health check endpoint to API for improved service monitoring

### Fixed

- **CriteriaType**: Seed genre and tag criteria types in migration so reference genre tree load-example and other flows no longer raise DoesNotExist
  - Add data migration `0003_seed_criteria_types` to ensure `CriteriaType` rows with pk 0 (genre) and 1 (tag) exist

### Improved

- **Deployment**: Apply Django migrations on every container start
  - Entrypoint always runs `migrate` after DB is ready (first init and subsequent deploys)
  - Single code path; migrate is idempotent

- **Entrypoint**: Use init-django-data instead of reinit when Django is not initialized
  - Prevents DROP USER / database purge on deploy when the init check fails or on first run
  - Reinit (purge + init) remains for manual use only; container only runs init (create DB/role if missing, migrate, fixtures)

- **init-django-data.sh**: Follow best practices for migrations
  - Only run `makemigrations` if no migration files exist (e.g., after purge)
  - In production/normal init, migrations should already be in repo; only `migrate` runs
  - Capture and log migrate output for better debugging
  - Exit with error code if makemigrations or migrate fails

- **check_data_initialized**: Handle missing tables gracefully
  - Check if User table exists before querying it (prevents ProgrammingError)
  - Properly detect "not initialized" state when tables don't exist
  - Better error messages for debugging

- **entrypoint.sh**: Improve migration error visibility
  - Capture and log migrate output to diagnose migration failures
  - Show exit code when migrations fail

- **check-django-initialized.sh**: Show check command output
  - Display check_data_initialized output instead of hiding it
  - Better visibility into why initialization check passes/fails
### Documentation

- **CONTRIBUTING.md**: Add Database migrations section (create in dev, never makemigrations in prod, migrations run on deploy, backward-compatibility)
- **workflows.md**: Document that migrations are applied by container entrypoint, not by deploy workflow

## [v0.3.6] - 2026-02-06

### CI

- **Versioning**: Derive app version from git tags instead of GitHub repository variables
  - Extract version from git tags in publish.yml workflow (supports pre-release versions: rc, beta, alpha, dev)
  - Pass app_version as input to reusable workflows (static-files, build, deploy, test)
  - Add version extraction logic with fallback to latest git tag
  - Remove dependency on APP_VERSION GitHub repository variable
  - Enables testing Docker images on test server using pre-release tags (e.g., v0.3.5-rc1)

- **Static Files Workflow**: Improve branch detection and conflict handling
  - Fail workflow if branch has newer commits on remote (prevents conflicts and data loss)
  - Check branch sync status before collecting static files and before committing
  - Improved branch detection for release branches and tag-triggered workflows
  - Better error handling with clear messages when branch is out of sync
  - Reorder workflow steps: checkout and verify branch sync before collecting static files

- **Workflows**: Remove workflow_dispatch manual triggers from all workflows
  - Workflows can only be triggered via workflow_call or automatic triggers (push, pull_request, tags)
  - Removes manual triggering capability from GitHub Actions UI
  - Ensures workflows are only triggered through proper channels

### Documentation
- **Dev tags**: remove overlapping document `dev-tag-practices.md`
- **Versioning Strategy**: Add comprehensive versioning.md documentation
  - Document git tag-based versioning approach
  - Explain pre-release version identifiers (rc, beta, alpha, dev) and their usage
  - Document version extraction logic and workflow inputs
  - Update workflows.md to reference versioning approach

- **Dev Tag Practices**: Add comprehensive dev tag documentation and cursor rule
  - Document dev tag naming convention (use branch name without type prefix)
  - Explain version selection strategy (placeholder based on branch type)
  - Provide guidance for republishing dev tags after changes
  - Add cleanup step to release process for removing dev tags
  - Create cursor rule to ensure consistent dev tag practices

## [v0.3.5] - 2026-02-04

### Fixed

- **Production Import Error**: Fix ModuleNotFoundError when importing User model in production
  - Move test utility import (`UploadedTrackTestFilename`) from module level to inside method
  - Prevents import error when `api.test` module is not available in production environment

## [v0.3.4] - 2026-02-04

### Fixed

- **API Schema Generation**: Fix Swagger UI Internal Server Error when accessing `/api/schema/`
  - Handle `list` action in `AppModelViewSet.get_serializer_class()` for drf-spectacular introspection
  - Add authentication check in `queryset` property to handle `AnonymousUser` during schema generation
  - Explicitly define `GeneratedField` as `DecimalField` in `FileDetailedSerializer` to prevent introspection errors
  - Add `SerializerMethodField` for nested JSON fields in `SpotifyUserDetailedSerializer` (display_name, followers, href, images, type, uri)

- **CI**: Add SPOTIFY_CLIENT_ID and SPOTIFY_CLIENT_SECRET to deploy workflow
  - Spotify credentials are now written to API .env file on server deployment
  - Fixes Django initialization failure when Spotify integration is enabled

- **CI**: Pass secrets to static-files workflow in publish workflow
  - Added `secrets: inherit` to publish workflow so STATIC_FILES_PAT token is available
  - Enables static files workflow to bypass branch protection when using PAT token

- **Git Worktree Configuration**: Added environment file (`env/.env`) to worktree copy configuration
  - Environment files are now automatically copied when creating new git worktrees
  - Improves developer experience by eliminating manual environment file setup

## [v0.3.3] - 2026-02-04

### Fixed

- **CI**: Handle detached HEAD when pushing static files from tag-triggered workflow
  - Static files workflow now detects detached HEAD state and checks out the appropriate branch (main/develop) before committing and pushing
  - Fixes workflow failure when publish workflow is triggered by version tags

## [v0.3.2] - 2026-02-04

### Fixed

- **Docker**: Correct fixture copy paths in Dockerfile to match repository layout
  - Copy from `app/` and `genres/` instead of non-existent `api/`; fixes build failure during image build

- **Docker**: Use python:3.14-bookworm base image instead of python:3.14-buster
  - python:3.14-buster is not published on Docker Hub; Python 3.14 images use Bookworm or Trixie

### Changed

- **Docker**: Run filesystem setup in entrypoint instead of Dockerfile so volume-mounted paths get correct permissions at container start

- **Docker Compose generation**: AFP container working_dir set to /app/ in generate-docker-compose-parts.sh (was /api/)

- **Docker**: Split image build into separate RUN steps for maintainability
  - System deps, Python deps, filesystem setup, and fixture copy each in their own step; easier to debug and reuse layers

- **Repository References**: Updated deploy workflow and package.json to use BehindTheMusicTree org
  - Deploy workflow redeployment webhook calls BehindTheMusicTree/github-workflows
  - package.json repository, bugs, and homepage URLs point to BehindTheMusicTree/the-music-tree-api

### CI

- **Workflows**: Add check-vars-and-secrets job to deploy, build, test, and static-files
  - Fails fast if required environment vars or secrets are missing; reports all missing ones (scripts/check-workflow-env.sh)

- **Publish Workflow**: Run only on version tags (v*) and manual/workflow_call dispatch; removed push-to-branch trigger

- **Deploy Workflow**: Use SERVER_DEPLOY_USERNAME secret instead of TEST_SERVER_BODZIFY_USERNAME for SSH destination

- **Deploy Workflow**: Remove SSH whitelist handling and scripts/whitelist-runner-ssh.sh

- **Test Workflow**: Run test workflow on push to main, develop, release/*, hotfix/*, chore/*
  - Ensures tests run on protected and chore branches without requiring a PR

- **Deploy Workflow**: Redeployment webhook calls BehindTheMusicTree/github-workflows; optional push trigger for chore/improve-cicd
  - Aligns CI/CD with BehindTheMusicTree organization

- **Workflow job names**: Shortened job names and publish job ids (static, build, deploy; Set env vars, Set compose files, Redeploy webhook; Static files, Push to Docker Hub) to reduce truncation in GitHub Actions UI
  - Aligned step name "Set up Python" in test workflow with static-files
  - docs/workflows.md documents job id and display name for each workflow

### Documentation

- **GitHub Actions Workflows**: Added docs/workflows.md documenting all workflows with table of contents
  - Describes triggers, steps, and environments for test, publish, build, deploy, static-files, branch-protection, labeler
  - CONTRIBUTING.md links to workflows doc in TOC and in Pull Request Process section
## [v0.3.1] - 2025-12-10

### Changed

- **Project Branding**: Updated references from Bodzify API to HearTheMusicTree API across documentation and configuration files
  - Updated README, VISION document, and various documentation files
  - Clarified project goals and mission statement

### Documentation

- **VISION Document**: Added comprehensive VISION.md document outlining project mission, goals, and principles
  - Describes integration with BehindTheMusicTree ecosystem
  - Outlines key principles: Personal-First, Metadata-First, Genre Intelligence, Privacy & Security, Interoperability, Accessibility
  - Documents ecosystem integration with AudioMeta Python, GrowTheMusicTree, and TheMusicTreeAPI

- **Project Presentation**: Improved project presentation across documentation
  - Updated README to better reflect HearTheMusicTree branding
  - Enhanced clarity of project goals and vision

### CI

- **Branch Protection**: Updated branch protection rules to allow `release/*` branches to target `develop`
  - Aligns with standard Git Flow workflow where release branches merge into both `main` and `develop`
  - Fixes issue where release branches couldn't merge back into `develop` due to branch protection rules

- **VS Code Settings**: Fixed JSON syntax errors in `.vscode/settings.json` and removed deprecated `python.pythonPath` setting
  - Removed trailing commas causing JSON parsing issues
  - Removed deprecated `python.pythonPath` in favor of `python.defaultInterpreterPath`
  - Improves VS Code configuration maintainability

### Changed

- **Test Files Cleanup**: Removed outdated test files from `bodzify_api/test/utils/uploaded_track/files/` directory
  - Deleted 7 duplicate test files from old directory structure
  - All test files now properly located in `api/test/utils/uploaded_track/files/` after test reorganization
  - Reduces repository size and eliminates confusion from duplicate files

## [v0.3.0] - 2025-12-10

### Changed

- **Test Organization**: Reorganized test structure to align with DRF conventions
  - Moved all tests to `api/test/tests/` directory for cleaner organization
  - Unit tests organized by component type (filtering, middleware, serializer, utils, validator)
  - Integration tests organized by endpoint/resource (album, artist, auth, criteria, playlist, uploaded_track, etc.)
  - E2E tests organized by workflow (track_upload, genre_hierarchy, spotify, etc.)
  - Moved middleware and FilterSet tests from integration to unit tests
  - Removed redundant `view/` and `common/` directories from integration tests
  - Updated test documentation to reflect new structure

- **Audio Metadata**: Replaced audio metadata management module with `audiometa-python` (bumped to `0.8.1` in `requirements.txt`)
- **Dependencies**: 
  - Updated `Django` from 5.0.3 to 5.2.8
  - Updated `asgiref` from 3.7.2 to 3.8.1 for Django 5.2.8 compatibility
  - Updated `psycopg2-binary` from 2.9.5 to 2.9.11 for Python 3.14 compatibility
  - Updated `django-stubs` from 5.1.1 to 5.2.1 for Django 5.2.8 compatibility
  - Updated `django-filter` from 22.1 to 25.2 for Python 3.14 compatibility (fixes `pkgutil.find_loader` removal)
  - Updated `django-polymorphic` from 3.1.0 to 4.1.0 to resolve pkg_resources deprecation warning and ensure Django 5.2 compatibility
  - Removed `mutagen` from direct dependencies. No longer needed as direct dependency since all audio operations now use `audiometa-python`

### Documentation

- **Test Documentation**: Updated test README and contributing guide
  - Added comprehensive test structure documentation in `api/test/README.md`
  - Added table of contents to test README
  - Updated CONTRIBUTING.md to reference test README
  - Added unit test suggestions document with detailed test scenarios
  - Clarified distinction between unit, integration, and E2E tests

- **Project Management**: Added `TODO.md` for tracking future work and improvements
  - Categorized by priority (high, medium, low)
  - Organized by features, testing, and infrastructure

- **Contributing Documentation**: Comprehensive contributing guide with strict Git Flow workflow
  - Detailed branch naming and merging rules for `main`, `develop`, `feature/*`, `release/*`, `hotfix/*`, and `chore/*` branches
  - Installation and setup instructions
  - Code style guidelines and development best practices
  - Pre-PR checklist and review process
  - Release process documentation

- **Development Guidelines**: Added `DEVELOPMENT.md` with comprehensive coding standards
  - Code quality practices and conventions
  - Django best practices for models, serializers, views, and filtering
  - Type checking and error handling guidelines
  - Documentation standards

- **Cursor Rules**: Added AI assistant rules to enforce project standards
  - Git Flow workflow enforcement
  - Commit message convention (Conventional Commits)
  - Pull request title convention
  - Issue template usage guidelines
  - Pre-PR checklist enforcement
  - Issue descriptions in separate version-controlled files
  - PR descriptions in git-ignored directory for local drafting
  - Test naming convention and structure guidelines
  - Changelog best practices

- **README**: Simplified `README.md` to provide high-level overview with links to detailed documentation
  - Moved detailed setup instructions to `CONTRIBUTING.md`
  - Added badges for license, Python version, and Django version

- **Contributing Guide**: Reorganized installation steps in `CONTRIBUTING.md` for logical flow
  - Environment variables setup before scripts that use them
  - Improved step-by-step instructions clarity

- **License**: Added Apache License 2.0

- **Code of Conduct**: Added Contributor Covenant 2.1

### Added

- **Git Worktree Scripts**: Added npm `git-worktree-scripts` package (v1.4.0) for managing git worktrees
  - Includes `setup-worktree.sh` script for automated worktree setup with virtual environment and dependencies
  - Added `.git-worktree-copy` configuration for copying gitignored files to new worktrees
    - Copies `env/.venv` Python virtual environment
    - Copies fixture files from `api/fixtures/*.json`
  - Integrated filesystem setup into `setup-worktree.sh` for automatic directory and log file creation

### Fixed

- **Error Handling**: Fixed Python 3.14 compatibility issues with exception attribute access
  - Wrapped all `exception.detail` accesses in try-except blocks to handle `AttributeError` and `TypeError`
  - Added safe stringification fallbacks for all `str(exception)` calls
  - Fixed `TypeError: 'super' object has no attribute 'dicts'` error in exception logging middleware
  - Updated `ErrorResponse`, `AppValidationException`, `AppSerializer`, `ExceptionLoggingMiddleware`, and `RequestLoggingMiddleware` to safely handle DRF exceptions in Python 3.14
  - Prevents middleware crashes when exception stringification fails

- **Filesystem Setup**: Fixed `setup-filesystem.sh` to check for `DJANGO_LOG_DIR` instead of `DJANGO_LOGS_DIR` to properly create log directories
  - Updated app name to 'api'

- **Filter Backend**: Added `get_schema_operation_parameters` method to `ConsistentParametersFilterBackend` for drf-spectacular compatibility with django-filter 25.2

- **Django 6.0 Compatibility**: Replaced deprecated `CheckConstraint.check` with `condition` parameter in all model constraints
  - Updated 6 model files: `CriteriaType`, `Criteria`, `Artist`, `Album`, `FingerprintMissingCauseCode`, `ManualPlaylist`
  - Updated migration file `0001_initial.py` to use new syntax
  - Resolves Django 6.0 deprecation warnings for `CheckConstraint.check`

- **Criteria Tree Import**: Removed debug print statements from `import_criteria_tree` method that were causing test hangs
  - Eliminated excessive I/O overhead when processing large tree imports (30,000+ nodes)
  - Fixed test hangs and significantly improved performance for large tree import operations

### CI

- **Test Configuration**: Filtered ResourceWarnings about unclosed files from Django's ORM in pytest configuration
  - Added `ignore:unclosed file:ResourceWarning` filter to `pytest.ini`
  - These warnings are non-actionable as they originate from Django's internal FileField handling
  - Improves test output clarity by reducing noise from Django ORM file handle management
  - Django automatically manages these file handles through garbage collection

- **GitHub Automation**:
  - Auto-labeler workflow (`.github/workflows/labeler.yml`) for automatic PR labeling based on file paths
  - Branch protection workflow (`.github/workflows/branch-protection.yml`) to enforce Git Flow rules
    - Blocks PRs to `main` from non-hotfix/release branches
    - Blocks PRs to `develop` from invalid branch types
  - Issue templates for bug reports and feature requests
  - Pull request template with comprehensive checklist
  - GitHub Discussions setup with category templates

- **Branch Protection**: Added automated enforcement of Git Flow branching rules
  - PRs to `main` must come from `hotfix/*` or `release/*` branches only
  - PRs to `develop` must come from `feature/*`, `chore/*`, or `dependabot/*` branches only
  - Provides clear error messages when branch rules are violated

- **CI Workflow**: Split monolithic CI workflow into focused, reusable workflows
  - Updated `test.yml` workflow to run tests on pushes and pull requests (removed redundant `ci.yml` wrapper)
  - Added fail-fast flag (`-x`) to pytest for faster CI feedback on test failures
  - Created `static-files.yml` workflow for collecting and pushing static files
  - Created `build.yml` workflow for Docker image building and pushing
  - Created `deploy.yml` workflow for server deployment tasks
  - Created `publish.yml` workflow for releases (triggers on version tags `v*`)
  - Publishing workflow handles static files collection, Docker build, and deployment
  - Improved workflow maintainability and reusability
  - Separation of concerns: tests run on every change, publishing only on releases

- **CI/CD**: Updated GitHub Actions workflow to use `develop` branch instead of `dev`
  - Updated Python version to 3.14 in CI workflows
  - Added branch protection checks for Git Flow enforcement

## [v0.2.0] - 2025-04-03

### Added
- Enable Spotify integration with comprehensive API support:
  - Track search and lookup by ID/ISRC
  - Artist information retrieval
  - Audio features analysis (tempo, key, energy, danceability)
  - Spotify OAuth authentication for user accounts
  - Track preview URL support
  - Album information integration
  - Artist popularity and genre data

## [v0.1.3] - 2025-04-02

### Added
- Enable genre tree JSON import
- Enable genre tree JSON export
- Enable delete criteria

### Changed
- Arrays in JSON must be without [] and in multipart with []

## [v0.1.2] - 2025-03-11

### Added
- Enable track archiving
- Complete filtering for all list requests
- Handle more tags formats: ID3v1 (.mp3, .wav, .flac), RIFF (wav)
- Implement a complete and consistent error handling system with precise codes (validation codes for bad requests)

### Changed
- Put all test files in same directory with consistent naming
- Set app not to handle in memory files: small files are handle as regular files

## [v0.1.1] - 2024-09-06

### Added
- Fingerprint check