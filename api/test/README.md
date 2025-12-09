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
  - [Warning Filters](#warning-filters)

## Test Categories

### Unit Tests (`tests/unit/`)

Unit tests test individual functions, classes, or modules in isolation with mocked dependencies.

**Location:** `api/test/tests/unit/`

**Organization:** Unit tests are organized by component type to mirror the codebase structure:
- `tests/unit/model/` - Model tests (business logic, methods, properties)
- `tests/unit/serializer/` - Serializer tests (validation, field behavior)
- `tests/unit/utils/` - Utility function tests
- `tests/unit/middleware/` - Middleware component tests
- `tests/unit/validator/` - Validator tests

**Examples:**
- `tests/unit/utils/audiometa_adapter/` - Tests for audiometa adapter functions
- `tests/unit/utils/file_path_utils/` - Tests for file path utility functions
- `tests/unit/validator/` - Tests for validators
- `tests/unit/serializer/field/` - Tests for serializer field classes
- `tests/unit/middleware/` - Tests for middleware components

**Characteristics:**
- Fast execution
- No database access (or minimal, isolated database usage)
- Mocked external dependencies
- Test single functions/methods/classes in isolation

### Integration Tests (`tests/integration/`)

Integration tests test how multiple components work together through API endpoints. These tests verify that the full request/response cycle works correctly, including middleware, serializers, views, and database interactions.

**Location:** `api/test/tests/integration/`

**Organization:** Integration tests are organized by API endpoint/resource:
- `tests/integration/` - API endpoint tests organized by resource
  - `uploaded_track/` - Uploaded track endpoints
  - `playlist/` - Playlist endpoints
  - `criteria/` - Criteria/genre endpoints
  - `artist/` - Artist endpoints
  - `common/` - Cross-cutting concerns tested through endpoints (e.g., security, duplicate fields)
  - etc.

**Examples:**
- `tests/integration/uploaded_track/` - Tests for uploaded track API endpoints
- `tests/integration/playlist/` - Tests for playlist API endpoints
- `tests/integration/criteria/` - Tests for criteria/genre API endpoints
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
- Audio metadata analysis fixture
- Test user directory cleanup

### Warning Filters

The pytest configuration (`pytest.ini`) includes filters to suppress non-actionable warnings:

- **ResourceWarnings for unclosed files**: Filtered to reduce noise from Django's ORM file handling
  - These warnings occur when Django's ORM accesses `FileField` values internally
  - Django manages these file handles automatically through garbage collection
  - The warnings are non-actionable and originate from Django's internal code, not application code
  - Filter: `ignore:unclosed file:ResourceWarning`

This configuration improves test output clarity while still showing actionable warnings from application code.


