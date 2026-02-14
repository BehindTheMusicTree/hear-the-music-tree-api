# {{RESOURCE_NAME}}

## Overview
{{SHORT_DESCRIPTION_OF_RESOURCE}}

## Base URL
{{BASE_URL}}

## Authentication
{{AUTHENTICATION_MECHANISM}}

## Permissions
{{PERMISSION_CLASSES_AND_RULES}}

## Endpoints
| Method | Path | Action | Description |
|------|------|--------|-------------|
{{ENDPOINT_TABLE}}

## Request / Response

{{FOR_EACH_ENDPOINT}}

### {{METHOD}} {{PATH}}

**Description**
{{WHAT_THE_ENDPOINT_DOES}}

**Request**
Headers:
{{REQUIRED_HEADERS}}

Query params:
{{QUERY_PARAMS}}

Body:
```json
{{REQUEST_EXAMPLE}}
```

**Response**
Status codes:
{{STATUS_CODES}}

Body:
```json
{{RESPONSE_EXAMPLE}}
```

### Validation Rules

{{SERIALIZER_VALIDATION_RULES}}

### Business Rules

{{NON_TECHNICAL_RULES}}

### Errors
| Code | Meaning |
|------|----------|
{{COMMON_ERRORS}}

### Versioning

{{API_VERSION_IF_ANY}}

### Notes

{{PERFORMANCE_OR_SECURITY_NOTES}}