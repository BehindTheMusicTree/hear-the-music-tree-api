# search

## Overview
Search across tracks, albums, artists, and playlists

## Base URL
/v1/search/

## Authentication
JWT token required

## Permissions
Authenticated users only (IsAuthenticated)

## Endpoints
| Method | Path | Action | Description |
|------|------|--------|-------------|
| GET | / | list | Search all resources |

## Request / Response

### GET /

**Description**
Search within tracks, albums, artists and playlists

**Request**
Headers:
Authorization: Bearer {token}

Query params:
query (search string)

Body:
None

**Response**
Status codes:
 | 00 OK

Body:
```json
{
  "uploaded_tracks": [
    {
      "uuid": "uuid",
      "relative_url": "string",
      "title": "string",
      "file": {},
      "artists": [],
      "album": {},
      "track_number": 1,
      "genre": {},
      "rating": 5,
      "language": "string",
      "playlists": [],
      "play_count": 0,
      "archived": false,
      "created_on": "2023-01-01T00:00:00Z",
      "updated_on": "2023-01-01T00:00:00Z"
    }
  ],
  "manual_playlists": [
    {
      "uuid": "uuid",
      "name": "string"
    }
  ],
  "criteria_playlists": [
    {
      "uuid": "uuid",
      "name": "string"
    }
  ],
  "albums": [
    {
      "uuid": "uuid",
      "name": "string",
      "year": 2023
    }
  ],
  "artists": [
    {
      "uuid": "uuid",
      "name": "string"
    }
  ]
}
```

### Validation Rules
None

### Business Rules
None

### Errors
Code	Meaning
 | 00	Bad Request - Invalid parameters
 | 01	Unauthorized - Invalid token

### Versioning

API path prefix uses the major version only (e.g. `v1`), derived from `APP_VERSION`.

### Notes
None