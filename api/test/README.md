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

**Examples:**
- `tests/unit/utils/audiometa_adapter/` - Tests for audiometa adapter functions
- `tests/unit/utils/file_path_utils/` - Tests for file path utility functions
- `tests/unit/validator/` - Tests for validators

**Characteristics:**
- Fast execution
- No database access
- Mocked external dependencies
- Test single functions/methods

### Integration Tests (`tests/integration/`)

Integration tests test how multiple components work together, typically through API endpoints.

**Location:** `api/test/tests/integration/`

**Examples:**
- `tests/integration/view/uploaded_track/` - Tests for uploaded track API endpoints
- `tests/integration/middleware/` - Tests for middleware components
- `tests/integration/private_resource/` - Tests for private resource filtering
- Tests that verify metadata reading/writing through the full API stack

**Characteristics:**
- Use database
- Test API endpoints
- Test component interactions
- May use real file operations

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


