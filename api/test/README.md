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

**When do e2e tests hit real services?** In CI (`ENV=ci_test`), all optional services (Spotify, Google OAuth, MusicBrainz) are **enabled with fake/placeholder credentials** and **mocked at the boundary** for all tests (including e2e), so no real provider calls are made. AFP is not mocked for e2e, so AFP e2e runs against the real AFP service in CI. E2e tests that need real Spotify/Google/MusicBrainz only hit those providers when run **locally** with real credentials.

**All optional services must be enabled:** The test run fails at collection if any of `SPOTIFY_ENABLED`, `GOOGLE_OAUTH_ENABLED`, or `MUSICBRAINZ_LOOKUP_ENABLED` is false. Set them to true in env (CI: workflow; dev: .env) and use fake credentials if not calling real APIs. Conftest only applies boundary mocks; it does not override env to enable services.

**Fail early (e2e):** When the run includes e2e tests, the session also checks that required services are reachable. In **CI**, only AFP must be reachable (others are mocked). In **dev**, every enabled service must be reachable.

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

Spotify and Google OAuth are mocked at the view layer via an autouse fixture. Env must have both enabled; the fixture only applies the boundary mock (no override). Tests that need the disabled branch use `@override_settings(SPOTIFY_ENABLED=False)` or `GOOGLE_OAUTH_ENABLED=False`.

- **When ENV=ci_test**: OAuth is mocked for **all** tests (unit, integration, and e2e). No real credentials or network calls.
- **In dev**: OAuth is mocked only for **non-e2e** tests. E2E tests are not mocked so you can run them with real Spotify/Google or per-test mocks locally.

E2E tests that need a specific OAuth response can patch the view’s service class as usual; in CI they will still see the global mock unless they override it.

#### Spotify API client mocking

The Spotify Web API client (`SpotifyClient` used for library, search, playlists, artist batch) is mocked via an autouse fixture so tests do not call the real Spotify API. Uses the same rule as OAuth.

- **When ENV=ci_test**: Spotify client is mocked for **all** tests.
- **In dev**: Mocked only for **non-e2e** tests; e2e tests can use the real API or their own mocks.

The mock returns empty lists/items for search, saved tracks, playlists, and artist batch. Tests that need specific responses patch `SpotifyClient` (or the manager) in their scope.

#### Audio meta analysis mocking

Audio meta analysis is the flow that uses AFP (fingerprinting) and MusicBrainz (AcoustID) lookup. AFP and MusicBrainz can be enabled independently (`AFP_ENABLED`, `MUSICBRAINZ_LOOKUP_ENABLED`). Both are mocked so non-e2e tests run that path without real external calls. E2E tests are not mocked and can use real AFP in CI.

- **MusicBrainz**: Env must have `MUSICBRAINZ_LOOKUP_ENABLED` true; conftest mocks `acoustid.lookup` (returns no results). Tests that need the disabled branch use `@override_settings(MUSICBRAINZ_LOOKUP_ENABLED=False)`. Tests that patch `acoustid.lookup` with a custom response use `@pytest.mark.patches_musicbrainz_lookup` and patch `api.utils.musicbrainz.service.acoustid.lookup`.
- **AFP (non-e2e only)**: Env must have `AFP_ENABLED` true; conftest only mocks `get_fingerprinting_result` for non-e2e. E2e: no mock (real AFP).
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


