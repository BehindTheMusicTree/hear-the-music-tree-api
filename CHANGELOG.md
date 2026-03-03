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
- **Spotify library sync**: Fixed Spotify library sync

### CI

- **Branch Protection**: Added automated enforcement of Git Flow branching rules
  - Blocks invalid PRs to main and develop branches
```

**Note:** During releases, maintainers will move entries from `[Unreleased]` to a versioned section (e.g., `## [0.2.8] - 2025-01-XX`).

## [Unreleased]

### Removed

- **Reference Spotify library**: Removed reference Spotify library API (`/v1/reference/library/spotify/`) and `ReferenceSpotifyLibTrackViewSet`. Exposing one Spotify account’s library to all users would violate Spotify’s User Guidelines and Developer Policy (no account sharing; each user must link their own account). Per-user Spotify library remains under `me/library/spotify/`. Documented in [Spotify compliance](docs/integrations/spotify.md#no-shared-system-spotify-account).

### Changed

- **Dependencies**: Bumped `audiometa-python` from 1.0.0 to 1.1.0.
- **E2E tests**: Refactored to one inheritance per domain with composition: added `_domain_helper()` on `AppTestCase`, introduced `SearchMixin`, and refactored multi-inheritance E2E tests to use a single domain base plus composed helpers. Corrected `ManualPlaylistTestCase` URL names to `me-manual-playlist-list` / `me-manual-playlist-detail`.
- **Fingerprint integration test**: `test_audio_fingerprinter_service_down_then_corresponding_missing_cause` now mocks `post_fingerprint_audio` to simulate service down instead of stopping a Docker container; no Docker required, runs in CI/sandbox.
- **MusicBrainz integration test**: `test_no_matching_recording_then_corresponding_missing_cause` now mocks `acoustid.lookup` to return an unknown error code so the test is deterministic; no network required, avoids flakiness when DNS/connection fails (code 8) instead of the expected unknown-response path (code 6).
- **Track URL validation**: `TrackUrlValidator` now accepts both HTTP 200 and 206 when checking that a track URL is reachable (Range request). Many servers respond with 200 when they do not support Range or after redirects; added timeout and narrowed exception handling to `requests.RequestException`.
- **Uploaded track title test**: `test_not_providing_title_nor_artist_and_original_filename_too_long_then_generate_with_app_prefixe` now mocks `requests.get` and `_download_file_from_url` so the test is deterministic and does not require network (runs in CI/sandbox). The real e2e test lives under `tests/e2e/track_upload/test_create_from_url_with_long_filename.py` and skips when the URL is unreachable.
- **Pytest**: Registered `e2e` marker in conftest. Documented that e2e tests live in `tests/e2e/` (directory split by test level) and can be run with `pytest api/test/tests/e2e/` or `pytest -m e2e` (CONTRIBUTING and api/test/README.md).
- **E2E tests**: Additional tests now use `_domain_helper()` for composed test cases (criteria playlist, manual playlist, genre hierarchy, tag-based playlist) to avoid duplicate user creation and `IntegrityError`. Manual playlist e2e expects 405 for DELETE (API does not support delete). Spotify OAuth e2e assertions use camelCase response keys and `to_camel_case`; final step uses `me-playlist-list`. MusicBrainz lookup failure e2e uses `RECORDING_TOKYO_DRIFT_NO_MB_RECORDING_MP3` and updated allowed missing-cause codes.
- **Unit (TrackFileValidator)**: `test_file_too_small_then_raises_app_validation_exception` now mocks min file size so it always runs in CI (no skip when config min is 0).
- **Integration (MusicBrainz)**: Added `test_drown_7m21_mp3_with_mocked_lookup_then_ok` with mocked `acoustid.lookup` so the recording-ID success path is covered in CI without network.
- **OAuth mocking**: When `ENV=CI_TEST`, Spotify and Google OAuth are mocked for all tests (including e2e). In dev, they are mocked only for non-e2e tests so e2e can use real OAuth locally. Documented in `api/test/README.md` and CONTRIBUTING.
- **OAuth optional in CI**: `SPOTIFY_OAUTH_ENABLED` and `GOOGLE_OAUTH_ENABLED` (default false) control whether Spotify/Google OAuth env vars are required. When false or unset, credentials are loaded optionally; auth views return 503 with "not configured" if called. CI test workflow sets both to false so OAuth vars are not needed. Added `load_optional_str_env_var` and `load_optional_secret_env_var` in env_var_loader.

### Documentation

- **API docs**: Aligned audio metadata endpoint in `docs/api/index.md` and `docs/api/audio_metadata.md` with actual path `/v1/audio/metadata/full/`.

## [v2.1.0] - 2026-02-23

### Added

- **Audio Metadata**: Added POST to get full raw metadata from a file

## [v2.0.1] - 2026-02-22

### Fixed

- **Deploy**: Requests to the bare domain (e.g. `themusictree.org`) and `www` no longer trigger `DisallowedHost`. Deploy workflow now adds the domain and `www.${DOMAIN_NAME}` to `ALLOWED_HOSTS` and `CSRF_TRUSTED_ORIGINS`.
- **Request logging**: Fixed "Error reading request body: You cannot access body after reading from request's data stream" on multipart requests (e.g. track upload to `uploaded/`). RequestLoggingMiddleware no longer reads `request.body` for `multipart/form-data` and logs a placeholder instead. Includes unit test.

- **Spotify OAuth**: Fixed backend always returning the same Spotify user regardless of which account completed login. Spotipy’s token cache was used by default, so the first user’s token was returned for every subsequent code exchange. The code exchange now uses `check_cache=False` so each login uses the provided authorization code.

### Removed

- **Admin**: SpotifyUser is no longer registered in Django admin (model was removed in v2.0.0 unified account).

### Changed

- **Dev env example**: `APP_NAME` default set to `htmt-api` (was `htmt_api`).
- **Scripts**: `run-db-and-afp-containers.sh` loads `env/.env` when present before running containers; `utils.sh` env loader trims keys and skips lines starting with `#`; `purge-django-data` cleanup (removed unused variable and redundant debug logs).

### Improved

- **Spotify OAuth**: When Spotify returns 403 "user may not be registered" (app in Development mode), the API now returns 401 with error code **1007** (`spotify_user_not_allowlisted`) and a clear user-facing message so the frontend can show a specific message without parsing. Docs and tests updated.

## [v2.0.2] - 2026-02-21

### Fixed

- **Spotify auth**: When Spotify returns `invalid_client` (e.g. wrong/missing app credentials), API now returns 500 with a generic "Sign-in is temporarily misconfigured" message instead of 401, since the failure is server configuration, not the user

### Changed

- **CI / Deploy**: Differentiate DB container port from host port: use `DB_PORT_CONTAINER` (and `DB_PORT_HOST`) instead of a single `DB_PORT` in workflows, Docker Compose generation, and env files
- **CI / Deploy**: Standardize container root path to `/home/app/` (`CONTAINER_ROOT_DIR`) across deploy, test, and static-files workflows
- **Dockerfile**: Remove `PROJECT_DIR` build arg; set `PROJECT_DIR=/home/app/` and `API_DIR_NAME=api` in image; build-and-push no longer passes `PROJECT_DIR`
- **Deploy (env and docker-compose)**: Set `FRONT_HOST` per environment (prod vs test) for Spotify/Google redirect URIs; add Django log directory and log filenames to API env file and workflow inputs; simplify env echo for client IDs (no extra quotes)
- **Deploy (docker-compose)**: DB and AFP compose parts use `DB_PORT_CONTAINER`; AFP healthcheck uses `AFP_PORT` instead of `APP_PORT`
- **Scripts**: `init-django-data.sh` validates `API_DIR_NAME` is a relative path (reject leading `/`)

## [v2.0.1] - 2026-02-20

### Changed

- **Deploy (env and docker-compose)**: API app env and reusable workflow input now set `APP_PORT` from `HTMT_API_PORT_TEST` when deploying to test and `HTMT_API_PORT` when deploying to prod
- **Deploy (env and docker-compose)**: AFP env file now sets `APP_PORT` from `AFP_PORT_TEST` when deploying to test and `AFP_PORT_PROD` when deploying to prod

## [v2.0.0] - 2026-02-20

### Added

- **Google OAuth**: `POST auth/google/` endpoint to exchange Google authorization code for session tokens
  - Request: `{ "code": "<authorization_code_from_google_callback>" }`
  - Response: `{ accessToken, refreshToken, expiresAt }` (same shape as Spotify auth for a single session model on the frontend)
  - Backend exchanges code with `oauth2.googleapis.com/token`, fetches user info, creates or links user, issues JWT session
  - Env: `GOOGLE_CLIENT_ID`, `GOOGLE_CLIENT_SECRET`, `GOOGLE_REDIRECT_URI` (must match frontend redirect URI)
  - `GoogleAuthenticationException` mapped to 401; integration tests for view and OAuth service
- **Unified account (Option A)**: One user can have both Google and Spotify linked; backend links by email when the same person signs in with a second provider
  - Single `User` model with optional `spotify_id` and `google_id` (and provider tokens/profiles); `SpotifyUser` and `GoogleUser` subclasses removed
  - Spotify auth: find by `spotify_id`, else by email (link), else create. Google auth: same for `google_id` and email
  - Frontend guide: `docs/frontend/unified-account-and-linking.md`

### Changed

- **API URL prefix**: Path prefix uses the major version only (e.g. `v1/`), derived from `APP_VERSION`; full semantic version is no longer used in URLs. Changelog and docs (README, `docs/versioning.md`, `docs/api/*`, frontend guides) updated to describe and use `v1` consistently
- **Auth response**: Spotify and Google auth now return `expiresAt` (Unix timestamp in milliseconds) for client-side expiry handling; JWT util returns `expires_at_ms` from access token payload

## [v1.0.5] - 2026-02-15

### Changed

- **API**: Current user's Spotify profile endpoint moved from `users/spotify/` to `me/spotify/` for consistency with other "current user" resources (`me/artists`, `me/playlists`, etc.). Admin user management remains at `users/`.
  - Docs: `docs/api/me_spotify.md`, `docs/api/index.md`, `docs/frontend/authentication-and-spotify.md`, README updated
- **API (me/spotify)**: Removed `GET /me/spotify/{id}/` (retrieve). Only `GET /me/spotify/` is supported; it returns a list of 0 or 1 item (current user's profile). Retrieve by id was redundant since the only valid id is the current user's.

- **Spotify / Auth**: Consistent 401 vs 403 for me/spotify and Spotify-required endpoints
  - **401** when not logged in to the app (API code 1006, `authentication_required`): frontend should redirect to app login
  - **403** when logged in but Spotify not linked (API code 1005, `spotify_authorization_required`): frontend should redirect to Spotify OAuth
  - `IsAuthenticatedReturn401` permission returns 401 instead of DRF default 403 for unauthenticated requests to Spotify user endpoints
  - Exception handler converts PermissionDenied to 401 when request is unauthenticated (fallback)
  - `AUTH_SPOTIFY_NOT_AUTHENTICATED` (1005) mapped to 403; `AUTH_NOT_AUTHENTICATED` (1006) to 401
  - Frontend guide: `docs/frontend/authentication-and-spotify.md`; API doc `docs/api/me_spotify.md` updated with error codes and link

### Fixed

- **API / OpenAPI**: Decimal fields are serialized as JSON numbers via `AppModelSerializer`: model `DecimalField` and `GeneratedField` with decimal `output_field` map to `FloatField` so schema and response use `number` (fixes Zod/client type mismatch)
- **Test**: Unit test enforces that all model serializers (Meta.model) extend `AppModelSerializer` so decimal-as-number stays consistent
- **URL routing**: Spotify profile moved to `me/spotify` (no longer under `users/`), so no route conflict with BaseUserViewSet
- **Spotify**: Added SpotifyAuthenticationException to custom exception handler so Spotify auth failures return 401 JSON instead of 500 in DEBUG

### Improved

- **env**: Add SUPERADMIN and DEMO credentials to .env.dev.example for enhanced configuration

## [v1.0.4] - 2026-02-13

### Added

-  **Users**: Added SUPERADMIN and DEMO environment variables to deployment workflow for enhanced configuration

### Fixed

- **Workflow**:Improved branch detection in static-files workflow by excluding symbolic refs

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