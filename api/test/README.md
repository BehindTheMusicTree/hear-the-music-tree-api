# Test Structure

This directory contains tests organized into three categories: **unit**, **integration**, and **e2e**.

All test files are located in the `tests/` subdirectory to keep the test directory structure clean.

## Table of Contents

- [Test Categories](#test-categories)
  - [Unit Tests](#unit-tests-testsunit)
  - [Integration Tests](#integration-tests-testsintegration)
  - [E2E Tests](#e2e-tests-testse2e)
- [Running Tests](#running-tests)
- [Test Naming Convention](#test-naming-convention)
- [Test Configuration](#test-configuration)
  - [Mocking](#mocking)
    - [OAuth mocking](#oauth-mocking)
    - [Spotify API client mocking](#spotify-api-client-mocking)
    - [Audio meta analysis mocking](#audio-meta-analysis-mocking)
  - [Warning Filters](#warning-filters)

## Test Categories

### Unit Tests (`tests/unit/`)

Unit tests test individual functions, classes, or modules in isolation with mocked dependencies.

**Location:** `api/test/tests/unit/`

**Organization:** Unit tests are organized by component type to mirror the codebase structure:
- `tests/unit/filtering/` - FilterSet and filtering component tests
- `tests/unit/middleware/` - Middleware component tests
- `tests/unit/serializer/` - Serializer tests (validation, field behavior)
- `tests/unit/utils/` - Utility function tests
- `tests/unit/validator/` - Validator tests

**Examples:**
- `tests/unit/utils/audiometa_adapter/` - Tests for audiometa adapter functions
- `tests/unit/utils/file_path_utils/` - Tests for file path utility functions
- `tests/unit/validator/` - Tests for validators
- `tests/unit/serializer/field/` - Tests for serializer field classes
- `tests/unit/middleware/` - Tests for middleware components
- `tests/unit/filtering/filterset/` - Tests for FilterSet classes

**Characteristics:**
- Fast execution
- No database access (or minimal, isolated database usage)
- Mocked external dependencies
- Test single functions/methods/classes in isolation

### Integration Tests (`tests/integration/`)

Integration tests test how multiple components work together through API endpoints. These tests verify that the full request/response cycle works correctly, including middleware, serializers, views, and database interactions.

**Location:** `api/test/tests/integration/`

**Organization:** Integration tests are organized by API endpoint/resource:
- `tests/integration/album/` - Album endpoints
- `tests/integration/artist/` - Artist endpoints
- `tests/integration/auth/` - Authentication endpoints
- `tests/integration/criteria/` - Criteria/genre endpoints
- `tests/integration/play/` - Play history endpoints
- `tests/integration/playlist/` - Playlist endpoints
- `tests/integration/search/` - Search endpoints
- `tests/integration/spotify/` - Spotify integration endpoints
- `tests/integration/uploaded_track/` - Uploaded track endpoints
- `tests/integration/user/` - User management endpoints
- etc.

**Examples:**
- `tests/integration/uploaded_track/` - Tests for uploaded track API endpoints
- `tests/integration/playlist/` - Tests for playlist API endpoints
- `tests/integration/criteria/` - Tests for criteria/genre API endpoints
- `tests/integration/auth/` - Tests for authentication endpoints
- Tests that verify the full API stack (middleware → serializer → view → database)

**Characteristics:**
- Use database (real or test database)
- Test complete API endpoints (HTTP methods: GET, POST, PUT, DELETE)
- Test component interactions (middleware, serializers, views working together)
- May use real file operations
- Test authentication and authorization
- Test error handling through the full stack

### E2E Tests (`tests/e2e/`)

End-to-end tests test complete user workflows and critical paths.

**Location:** `api/test/tests/e2e/`

**Examples:**
- `tests/e2e/track_upload/` - Complete track upload workflows
- `tests/e2e/genre_hierarchy/` - Genre hierarchy and playlist generation
- `tests/e2e/spotify/` - Spotify OAuth and library sync
- Full user workflows (upload → process → retrieve)
- Critical system integrations (audio fingerprinting, Spotify integration)

**Characteristics:**
- Full system tests
- Test complete workflows
- May include external service integrations
- Slower execution

Tests that need real external services (URLs, APIs) have a **mocked** version under `tests/integration/` (no network) and a **real** version under **`tests/e2e/`**. E2E tests are marked `@pytest.mark.e2e`. When run locally with the intent to hit real services, they **fail** (do not skip) when the service is unreachable so we investigate (config, network, service health). To avoid running e2e tests that need a service you have not configured, run a subset (e.g. `pytest api/test/tests/integration/`) or exclude the e2e tests that require that service.

**When to add a real e2e test:** Add at least one **real** e2e test for the same behaviour when the service can be exercised without blocking CI: e.g. the service is under our control (AFP in CI) or the test fails when the third-party service is unreachable (so we investigate). Put it under **`tests/e2e/`**, mark it `@pytest.mark.e2e`, perform the real request, and **fail** (do not skip) when the service is unreachable when run in an environment where the service is expected to be available.

**When do e2e tests hit real services?** In CI (`ENV=CI_TEST`), Spotify, Google OAuth, and MusicBrainz are mocked for all tests (including e2e), so those e2e tests only hit real providers when run **locally** with the corresponding services enabled. AFP is not mocked for e2e, so AFP e2e can run for real in CI if the AFP service is available.

**Fail early:** When the run includes e2e tests, the session checks that required services are reachable and exits immediately if not. In **CI** (`ENV=CI_TEST`), AFP must be enabled and reachable. In **dev**, every service that is enabled in config (Spotify, Google OAuth, AFP, MusicBrainz) must be reachable; if any is unreachable, the run fails with a clear message. Disabled services are not checked. This avoids running many tests only to have e2e fail later.

**AFP vs MusicBrainz:** AFP (fingerprinting) and MusicBrainz (AcoustID) lookup can be toggled independently via `AFP_ENABLED` and `MUSICBRAINZ_LOOKUP_ENABLED`. CI runs with AFP enabled and MusicBrainz disabled so e2e can hit real AFP without requiring ACOUSTID credentials or MB mocks for that path.

**Run e2e:** `pytest api/test/tests/e2e/` or `pytest -m e2e`.

## Running Tests

Run all tests:
```bash
pytest
```

Run specific category:
```bash
pytest api/test/tests/unit/
pytest api/test/tests/integration/
pytest api/test/tests/e2e/
```

Run specific test file:
```bash
pytest api/test/tests/unit/utils/audiometa_adapter/test_audiometa_adapter.py
pytest api/test/tests/integration/uploaded_track/test_post.py
```

Run tests for a specific component:
```bash
pytest api/test/tests/unit/serializer/
pytest api/test/tests/unit/utils/
pytest api/test/tests/integration/uploaded_track/
```

## Test Naming Convention

All test functions must follow the pattern: `test_{scenario}_then_{expected_result}`

Examples:
- `test_valid_mp3_extension_then_passes`
- `test_invalid_extension_then_raises_app_validation_exception`
- `test_id3v2_mp3_5_stars_then_10`

## Test Configuration

The test configuration is located in `api/test/tests/conftest.py` and includes:

- Test execution ordering (critical → unit → integration → e2e)
- Critical test failure handling
- Test user directory cleanup
- Mocking (OAuth, Spotify API client, audio meta analysis): see [Mocking](#mocking)
- Warning filters: see [Warning Filters](#warning-filters)

### Mocking

External services are mocked so CI and non-e2e tests do not call real providers. See below for each.

#### OAuth mocking

Spotify and Google OAuth are mocked at the view layer via an autouse fixture. When mocking, conftest also applies `override_settings(SPOTIFY_ENABLED=True, SPOTIFY_CLIENT_ID='test', ...)` and `GOOGLE_OAUTH_ENABLED=True, GOOGLE_CLIENT_ID='test', ...)` so the auth view paths run (same pattern as AFP/MusicBrainz). Tests that need the disabled branch use `@override_settings(SPOTIFY_ENABLED=False)` or `GOOGLE_OAUTH_ENABLED=False`. CI sets these to false in env so credentials are not required; the overrides apply only while the mock fixture is active.

- **When ENV=CI_TEST**: OAuth is mocked for **all** tests (unit, integration, and e2e). No real credentials or network calls.
- **In dev**: OAuth is mocked only for **non-e2e** tests. E2E tests are not mocked so you can run them with real Spotify/Google or per-test mocks locally.

E2E tests that need a specific OAuth response can patch the view’s service class as usual; in CI they will still see the global mock unless they override it.

#### Spotify API client mocking

The Spotify Web API client (`SpotifyClient` used for library, search, playlists, artist batch) is mocked via an autouse fixture so tests do not call the real Spotify API. Uses the same rule as OAuth.

- **When ENV=CI_TEST**: Spotify client is mocked for **all** tests.
- **In dev**: Mocked only for **non-e2e** tests; e2e tests can use the real API or their own mocks.

The mock returns empty lists/items for search, saved tracks, playlists, and artist batch. Tests that need specific responses patch `SpotifyClient` (or the manager) in their scope.

#### Audio meta analysis mocking

Audio meta analysis is the flow that uses AFP (fingerprinting) and MusicBrainz (AcoustID) lookup. AFP and MusicBrainz can be enabled independently (`AFP_ENABLED`, `MUSICBRAINZ_LOOKUP_ENABLED`). Both are mocked so non-e2e tests run that path without real external calls. E2E tests are not mocked and can use real AFP in CI.

- **MusicBrainz**: When mocking (CI or non-e2e), `override_settings(MUSICBRAINZ_LOOKUP_ENABLED=True)` is applied so the lookup path runs, and `acoustid.lookup` is mocked (returns no results). Same pattern as AFP: enable + mock in conftest. Tests that need the disabled branch use `@override_settings(MUSICBRAINZ_LOOKUP_ENABLED=False)`.
- **AFP (non-e2e only)**: `override_settings(AFP_ENABLED=True)` is applied so the path runs regardless of .env, and `get_fingerprinting_result` is mocked to return a successful result. E2e: no override, no AFP mock (real AFP allowed, e.g. in CI).
- **Tests that need real AFP** (e.g. critical AFP connection test): use `@pytest.mark.requires_real_afp` so the AFP mock is skipped.
- **Tests that need the disabled path**: use `with override_settings(AFP_ENABLED=False):` around the code that triggers the path (e.g. the upload call) so the disabled branch is taken.
- **Tests that need AFP enabled but MB disabled**: use `@override_settings(MUSICBRAINZ_LOOKUP_ENABLED=False)`; the app will run fingerprinting and set `MUSICBRAINZ_LOOKUP_DISABLED` as the MB missing cause.

### Warning Filters

The pytest configuration (`pytest.ini`) includes filters to suppress non-actionable warnings:

- **ResourceWarnings for unclosed files**: Filtered to reduce noise from Django's ORM file handling
  - These warnings occur when Django's ORM accesses `FileField` values internally
  - Django manages these file handles automatically through garbage collection
  - The warnings are non-actionable and originate from Django's internal code, not application code
  - Filter: `ignore:unclosed file:ResourceWarning`

This configuration improves test output clarity while still showing actionable warnings from application code.


