# Reference Genre Playlists

## Overview
Public endpoint to retrieve genre playlists owned by the system user (defined by TMTA_USERNAME environment variable).

## Base URL
/api/{APP_VERSION}/reference/genre-playlists/

## Authentication
None (public endpoint)

## Permissions
None

## Endpoints
| Method | Path | Action | Description |
|------|------|--------|-------------|
| GET | / | list | List reference genre playlists |

## Request / Response

### GET /

**Description**
List all genre playlists owned by the system user

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
 | 00

Body:
```json
[
  {
    "id": "string",
    "name": "string",
    "description": "string",
    // ... other fields from GenrePlaylist serializer
  }
]
```

### Validation Rules
TODO

### Business Rules
Returns only playlists owned by the system user (TMTA_USERNAME)

### Errors
Code	Meaning
 | 00	Bad Request
 | 04	Not Found

### Versioning
TODO

### Notes
This endpoint is public and does not require authentication. It provides reference genre playlists for public consumption.