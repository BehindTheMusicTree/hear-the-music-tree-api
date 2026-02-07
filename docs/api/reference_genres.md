# Reference Genres

## Overview
Public endpoint to retrieve genres owned by the system user (defined by TMTA_USERNAME environment variable).

## Base URL
`/api/{APP_VERSION}/reference-genres/`

## Authentication
None (public endpoint)

## Permissions
None

## Endpoints
| Method | Path | Action | Description |
|--------|------|--------|-------------|
| GET | / | list | List reference genres |

## Request / Response

### GET /

**Description**
List all genres owned by the system user

**Request**
Headers:
None

Query params:
TODO

Body:
```json
{}
```

**Response**
Status codes:
200 OK

Body:
```json
[
  {
    "uuid": "uuid",
    "name": "string",
    "parent": {},
    "ascendants": [],
    "descendants": [],
    "root": {},
    "children": [],
    "criteria_playlist": {},
    "uploaded_tracks": [],
    "uploaded_tracks_count": 10,
    "uploaded_tracks_archived_count": 0,
    "created_on": "2023-01-01T00:00:00Z",
    "updated_on": "2023-01-01T00:00:00Z"
  }
]
```

### Validation Rules
TODO

### Business Rules
Returns only genres owned by the system user (TMTA_USERNAME)

### Errors
| Code | Meaning |
|------|---------|
| 400 | Bad Request |
| 404 | Not Found |

### Versioning
TODO

### Notes
This endpoint is public and does not require authentication. It provides reference genres for public consumption.
