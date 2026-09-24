# Unit Test Suggestions

This document outlines suggested unit tests to improve test coverage across the codebase. Unit tests should test individual functions, classes, or modules in isolation with mocked dependencies.

## Priority Levels

- **High**: Critical functionality, error handling, or frequently used utilities
- **Medium**: Important but less critical functionality
- **Low**: Edge cases, convenience functions, or rarely used features

---

## Utils

### `hear/utils/json_utils.py` - **High Priority**

**Functions to test:**

- `transform_uuids(obj)` - Transform UUID objects to strings in nested data structures

  - Test with nested dictionaries containing UUIDs
  - Test with lists containing UUIDs
  - Test with mixed structures (dicts, lists, UUIDs)
  - Test with non-UUID values (should remain unchanged)
  - Test with empty structures
  - Test with deeply nested structures

- `UUIDJSONEncoder` - JSON encoder for UUID serialization
  - Test encoding UUID objects
  - Test encoding non-UUID objects (should use default behavior)
  - Test encoding nested structures with UUIDs

**Test file:** `hear/test/tests/unit/utils/json_utils/test_json_utils.py`

---

### `hear/utils/model.py` - **High Priority**

**Classes/Functions to test:**

- `SaveContext` dataclass

  - Test `create()` factory method with various kwargs
  - Test `should_track_fields` property (True when update_fields is not None)
  - Test `add_modified_field()` - adds to modified_fields
  - Test `add_modified_field()` - adds to update_fields when should_track_fields is True
  - Test `add_modified_field()` - doesn't add duplicate fields to update_fields

- `ensure_update_field(kwargs, field_name)` - Ensure field in update_fields

  - Test when update_fields doesn't exist (creates it)
  - Test when update_fields is None (creates it)
  - Test when update_fields exists (appends if not present)
  - Test when field already in update_fields (no duplicate)

- `ensure_update_fields(kwargs, field_names)` - Ensure multiple fields in update_fields
  - Test with multiple fields
  - Test with existing update_fields
  - Test with None update_fields
  - Test with duplicate prevention

**Test file:** `hear/test/tests/unit/utils/model/test_model_utils.py`

---

### `hear/utils/utils.py` - **Medium Priority**

**Functions to test:**

- `generate_short_uu(length)` - Generate short UUID-like string

  - Test with different lengths
  - Test that output contains only uppercase letters and digits
  - Test that output length matches input
  - Test randomness (multiple calls produce different results)

- `get_substring_after_last_slash(string)` - Extract filename from path

  - Test with full paths
  - Test with URLs
  - Test with no slashes (returns entire string)
  - Test with trailing slash

- `get_file_extension_from_url(url)` - Extract file extension
  - Test with various extensions
  - Test with URLs containing query parameters
  - Test with no extension
  - Test with multiple dots

**Test file:** `hear/test/tests/unit/utils/test_utils.py`

---

### `hear/utils/env_var_loader.py` - **High Priority**

**Functions to test:**

- `load_required_str_env_var(var_name, must_print_value)` - Load required string env var

  - Test with existing env var
  - Test with missing env var (raises EnvironmentError)
  - Test with `must_print_value=True` (prints value)
  - Test with `must_print_value=False` (prints "is set")

- `load_required_bool_env_var(var_name)` - Load required boolean env var

  - Test with "true" (returns True)
  - Test with "false" (returns False)
  - Test with invalid value (raises EnvironmentError)
  - Test with missing var (raises EnvironmentError)

- `load_required_int_env_var(var_name)` - Load required integer env var

  - Test with valid integer string
  - Test with invalid integer string (raises EnvironmentError)
  - Test with missing var (raises EnvironmentError)

- `load_required_path_env_var(var_name, must_print_value)` - Load required path env var

  - Test with existing path
  - Test with non-existent path (raises EnvironmentError)
  - Test with missing var (raises EnvironmentError)

- `load_required_secret_env_var(var_name)` - Load secret env var (strips quotes)
  - Test with quoted value (strips quotes)
  - Test with unquoted value (returns as-is)
  - Test with missing var (raises EnvironmentError)

**Note:** These tests will require mocking `os.getenv()` and `Path.exists()`

**Test file:** `hear/test/tests/unit/utils/env_var_loader/test_env_var_loader.py`

---

### `hear/utils/data_transformer.py` - **Medium Priority**

**Functions to test:**

- `remove_substrings_from_string(string_a, substrings)` - Remove substrings

  - Test removing single substring
  - Test removing multiple substrings
  - Test with overlapping substrings
  - Test with empty string

- `convert_data_to_dict(data)` - Convert QueryDict/dict to dict

  - Test with QueryDict
  - Test with dict
  - Test with other iterable (converts to dict)

- `to_camel_case(snake_str)` - Convert snake_case to camelCase

  - Test simple cases
  - Test with multiple underscores
  - Test with single word (no underscores)

- `to_snake_case(name)` - Convert camelCase/PascalCase to snake_case

  - Test camelCase
  - Test PascalCase
  - Test with acronyms
  - Test with numbers

- `dict_to_snake_case(data)` - Convert dict keys to snake_case

  - Test with dict
  - Test with QueryDict
  - Test with string (returns as-is)
  - Test nested conversion

- `get_copy_of_dict_including_only_specified_keys(data_dict, keys)` - Filter dict by keys

  - Test with existing keys
  - Test with missing keys (ignored)
  - Test with empty keys list

- `remove_none_or_empty_key_from_dict(data_dict)` - Remove None/empty values

  - Test with None values
  - Test with empty strings
  - Test with valid values (preserved)

- `update_dict_converting_empty_string_to_none(data)` - Convert "" to None

  - Test with empty strings
  - Test with None (unchanged)
  - Test with valid values (unchanged)

- `update_dict_converting_str_to_int_value_if_set(key, data)` - Convert string to int

  - Test with valid integer string
  - Test with invalid string (sets to None)
  - Test with empty string (sets to None)
  - Test with None (unchanged)

- `get_first_value_str_if_exists_in_str_dict_or_none(str_dict, key)` - Get first list value

  - Test with list (returns first)
  - Test with empty list (returns None)
  - Test with non-list value (returns value)
  - Test with missing key (returns None)

- `get_first_value_int_if_exists_in_str_dict_or_none(str_dict, key)` - Get first int value
  - Test with valid integer string
  - Test with invalid string (returns None)
  - Test with empty string (returns None)
  - Test with list containing valid int string
  - Test with missing key (returns None)

**Test file:** `hear/test/tests/unit/utils/data_transformer/test_data_transformer.py`

---

### `hear/utils/jwt.py` - **Medium Priority**

**Functions to test:**

- `create_jwt_token(user)` - Create JWT tokens for user
  - Test that access token is created
  - Test that refresh token is created
  - Test that expires_at is set (5 minutes from now)
  - Test with different users (different tokens)

**Note:** Requires mocking `RefreshToken.for_user()` and `AccessToken.for_user()`

**Test file:** `hear/test/tests/unit/utils/jwt/test_jwt.py`

---

### `hear/utils/audio_fingerprinter/` - **High Priority**

**Files to test:**

- `utils.py` - Utility functions for fingerprinting
- `service.py` - Fingerprinting service logic

**Test scenarios:**

- Fingerprint generation with valid audio
- Fingerprint generation failure handling
- Error code mapping
- Duration validation

**Test file:** `hear/test/tests/unit/utils/audio_fingerprinter/test_fingerprinter_utils.py`
**Test file:** `hear/test/tests/unit/utils/audio_fingerprinter/test_fingerprinter_service.py`

---

### `hear/utils/audio_file_metadata/` - **High Priority**

**Functions to test:**

- `is_flac_md5_valid(file_path)` - Validate FLAC MD5 checksum

  - Test with valid FLAC file
  - Test with invalid/corrupted FLAC file
  - Test with non-FLAC file (should handle gracefully)

- `fix_md5_checking(file_path)` - Fix MD5 checking for FLAC files
  - Test fixing corrupted MD5
  - Test with valid MD5 (no change needed)

**Note:** Requires actual FLAC files or mocking

**Test file:** `hear/test/tests/unit/utils/audio_file_metadata/test_flac_md5.py`

---

## Serializers

### Serializer Fields - **High Priority**

#### `AppEmailField` - **High Priority**

- Test valid email addresses
- Test invalid email formats
- Test None value with `allow_null=True`
- Test None value with `allow_null=False` (raises error)
- Test empty string with `allow_blank=True`
- Test empty string with `allow_blank=False` (raises error)
- Test non-string values (raises error)

**Test file:** `hear/test/tests/unit/serializer/field/test_app_email_field.py`

---

#### `AppUrlField` - **High Priority**

- Test valid URLs
- Test invalid URL formats
- Test None value handling
- Test empty string handling
- Test that it properly delegates to DRF's URLField

**Test file:** `hear/test/tests/unit/serializer/field/test_app_url_field.py`

---

#### `AppUuidField` - **High Priority**

- Test valid UUID strings
- Test invalid UUID formats
- Test None value with `allow_null=True`
- Test None value with `allow_null=False` (raises error)
- Test that it raises AppValidationException (not DRF ValidationError)

**Test file:** `hear/test/tests/unit/serializer/field/test_app_uuid_field.py`

---

#### `AppFileField` - **High Priority**

- Test valid file uploads
- Test invalid file types
- Test file size validation
- Test None value handling
- Test empty file handling

**Test file:** `hear/test/tests/unit/serializer/field/test_app_file_field.py`

---

#### `AppDictField` - **Medium Priority**

- Test valid dictionary values
- Test invalid types (not dict)
- Test nested validation
- Test None value handling

**Test file:** `hear/test/tests/unit/serializer/field/test_app_dict_field.py`

---

### Foreign Key Fields - **High Priority**

#### `PrivateUuidField` - **High Priority**

- Test with valid UUID owned by user
- Test with UUID not owned by user (raises error)
- Test with non-existent UUID (raises error)
- Test with None value handling
- Test user filtering logic

**Test file:** `hear/test/tests/unit/serializer/field/foreign_key/test_private_uuid_field.py`

---

#### `NonSelfReferencingField` - **High Priority**

- Test with valid parent UUID (different from self)
- Test with self-reference (raises error)
- Test with None value handling
- Test with non-existent UUID

**Test file:** `hear/test/tests/unit/serializer/field/foreign_key/test_non_self_referencing_field.py`

---

#### `DescendantAwareField` - **High Priority**

- Test with valid descendant UUID
- Test with ancestor UUID (raises error - circular reference)
- Test with self-reference (raises error)
- Test with None value handling
- Test complex hierarchy scenarios

**Test file:** `hear/test/tests/unit/serializer/field/foreign_key/test_descendant_aware_field.py`

---

#### `UserContentObjectUuidField` - **High Priority**

- Test with valid UUID owned by user
- Test with UUID not owned by user (raises error)
- Test with None value handling
- Test user filtering logic

**Test file:** `hear/test/tests/unit/serializer/field/foreign_key/test_user_content_object_uuid_field.py`

---

#### `TrackablePlayCountUuidField` - **Medium Priority**

- Test with valid trackable UUID
- Test with non-trackable UUID (raises error)
- Test with None value handling

**Test file:** `hear/test/tests/unit/serializer/field/foreign_key/test_trackable_play_count_uuid_field.py`

---

### Specialized Fields - **Medium Priority**

#### `RatingField` - **Medium Priority**

- Test valid rating values (0-10)
- Test out-of-range values (raises error)
- Test None value handling
- Test string to int conversion

**Test file:** `hear/test/tests/unit/serializer/field/test_rating_field.py`

---

#### `TrackNumberField` - **Medium Priority**

- Test valid track numbers
- Test invalid track numbers (negative, zero, too large)
- Test None value handling
- Test string to int conversion

**Test file:** `hear/test/tests/unit/serializer/field/test_track_number_field.py`

---

#### `UniquePerUserNameField` - **High Priority**

- Test with unique name for user
- Test with duplicate name for same user (raises error)
- Test with duplicate name for different user (allowed)
- Test with None value handling
- Test user filtering logic

**Test file:** `hear/test/tests/unit/serializer/field/test_unique_per_user_name_field.py`

---

#### `ArtistsNamesField` - **Medium Priority**

- Test with valid artist names list
- Test with empty list
- Test with duplicate names (if not allowed)
- Test with None value handling
- Test normalization logic

**Test file:** `hear/test/tests/unit/serializer/field/test_artists_names_field.py`

---

#### `TreeField` - **High Priority**

- Test with valid tree structure
- Test with invalid tree structure (raises error)
- Test with empty tree
- Test with circular references (raises error)
- Test with duplicate names (raises error)
- Test tree validation logic

**Test file:** `hear/test/tests/unit/serializer/field/test_tree_field.py`

---

### Serializer Classes - **Medium Priority**

#### `PutSerializer` - **Medium Priority**

- Test `validate()` method
- Test that it requires at least one field to be updated
- Test with empty data (raises error)
- Test with valid partial updates

**Test file:** `hear/test/tests/unit/serializer/test_put_serializer.py`

---

## Validators

### `TrackUrlValidator` - **High Priority**

**Test scenarios:**

- `__call__(value)` - Main validation method

  - Test with valid audio URL
  - Test with non-string value (raises AppValidationException)
  - Test with invalid URL format (raises error)
  - Test with invalid extension (raises error)
  - Test with non-existent remote file (raises error)

- `_validate_url_format(value)` - URL format validation

  - Test with http:// URLs
  - Test with https:// URLs
  - Test with non-http URLs (raises error)
  - Test with invalid URL format (raises error)

- `_validate_audio_extension(value)` - Audio extension validation

  - Test with valid extensions (from settings)
  - Test with invalid extensions (raises error)
  - Test case-insensitive matching

- `_validate_remote_file_exists(value)` - Remote file validation
  - Test with existing file (HTTP 206 response)
  - Test with non-existent file (HTTP 404, raises error)
  - Test with network error (raises error)
  - Test with non-206 status code (raises error)

**Note:** Requires mocking `requests.get()`

**Test file:** `hear/test/tests/unit/validator/test_track_url_validator.py`

---

## Middleware

### `CamelToSnakeMiddleware` - **High Priority**

**Test scenarios:**

- Test converting camelCase request data to snake_case
- Test converting camelCase query parameters to snake_case
- Test with nested dictionaries
- Test with lists
- Test with multipart form data
- Test that response is not modified
- Test with empty request data

**Note:** Requires Django test client or mocking request objects

**Test file:** `hear/test/tests/unit/middleware/test_camel_to_snake_middleware.py`

---

### `DuplicateFieldsMiddleware` - **Medium Priority**

**Test scenarios:**

- Test detecting duplicate fields in JSON requests
- Test detecting duplicate fields in multipart requests
- Test allowing list fields with [] suffix
- Test error response format
- Test with no duplicates (passes through)

**Note:** Some tests may already exist, but additional edge cases should be covered

**Test file:** `hear/test/tests/unit/middleware/test_duplicate_fields_middleware.py` (may already exist)

---

### `TestClientEmptyListMiddleware` - **Low Priority**

**Test scenarios:**

- Test normalizing [''] back to [] for list fields
- Test only processing requests with X-Test-Client header
- Test only processing POST requests
- Test with multipart form data
- Test with non-multipart data (no change)

**Test file:** `hear/test/tests/unit/middleware/test_client_empty_list_middleware.py`

---

### `HostValidationMiddleware` - **Medium Priority**

**Test scenarios:**

- Test with allowed hosts
- Test with disallowed hosts (raises error)
- Test error response format
- Test with missing host header

**Test file:** `hear/test/tests/unit/middleware/test_host_validation_middleware.py`

---

### `RequestLoggingMiddleware` - **Low Priority**

**Test scenarios:**

- Test that requests are logged
- Test log format
- Test with different request types
- Test with sensitive data (should be filtered)

**Note:** Requires mocking logger

**Test file:** `hear/test/tests/unit/middleware/test_request_logging_middleware.py`

---

### `ExceptionLoggingMiddleware` - **Low Priority**

**Test scenarios:**

- Test that exceptions are logged
- Test log format
- Test with different exception types
- Test that response is still returned

**Note:** Requires mocking logger

**Test file:** `hear/test/tests/unit/middleware/test_exception_logging_middleware.py`

---

## Exceptions

### `AppValidationException` - **High Priority**

**Test scenarios:**

- Test `__init__()` - Exception initialization

  - Test with all parameters
  - Test with default field name
  - Test error structure (errors dict format)
  - Test error_type marker

- Test `_detect_and_convert_from_drf_exception()` - DRF error detection
  - Test detecting AppValidationException in DRF ValidationError
  - Test with non-DRF exception (returns None)
  - Test with list error detail (converts to dict)
  - Test with nested error structures
  - Test with missing error_type marker (returns None)

**Test file:** `hear/test/tests/unit/exception/test_app_validation_exception.py`

---

### Spotify Exceptions - **Low Priority**

**Test scenarios:**

- Test `SpotifyException` base class
- Test `SpotifyAuthenticationException`
- Test `SpotifyResourceNotFoundException`
- Test `SpotifyRateLimitException`
- Test exception inheritance
- Test exception messages

**Test file:** `hear/test/tests/unit/exception/spotify/test_spotify_exceptions.py`

---

### MusicBrainz Exceptions - **Low Priority**

**Test scenarios:**

- Test `MusicbrainzRecordingLookupException` base class
- Test concrete exception classes
- Test `get_error_message()` method
- Test exception inheritance

**Test file:** `hear/test/tests/unit/exception/musicbrainz/test_musicbrainz_exceptions.py`

---

## Test Organization

All new unit tests should be placed in `hear/test/tests/unit/` following the existing directory structure:

```
hear/test/tests/unit/
├── utils/
│   ├── json_utils/
│   ├── model/
│   ├── env_var_loader/
│   ├── data_transformer/
│   ├── jwt/
│   ├── audio_fingerprinter/
│   └── audio_file_metadata/
├── serializer/
│   └── field/
│       ├── foreign_key/
│       └── criteria/
├── validator/
├── middleware/
└── exception/
```

## Testing Guidelines

1. **Isolation**: Each test should be independent and not rely on other tests
2. **Mocking**: Mock external dependencies (database, network, file system)
3. **Coverage**: Test both success and failure paths
4. **Edge Cases**: Test boundary conditions, None values, empty strings, etc.
5. **Naming**: Follow the pattern `test_{scenario}_then_{expected_result}`
6. **Assertions**: Use `assert` instead of `assertEqual`
7. **Single Scenario**: Each test should focus on a single scenario

## Priority Implementation Order

1. **Phase 1 (High Priority)**: Utils (json_utils, model, env_var_loader), Serializer Fields (AppEmailField, AppUrlField, AppUuidField, PrivateUuidField), Validators (TrackUrlValidator), Exceptions (AppValidationException)
2. **Phase 2 (Medium Priority)**: Remaining serializer fields, middleware (CamelToSnakeMiddleware, HostValidationMiddleware), Utils (data_transformer, jwt)
3. **Phase 3 (Low Priority)**: Logging middleware, exception classes, edge cases
