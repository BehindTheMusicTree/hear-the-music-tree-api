# Me Genre Playlists

## Overview
Manage genre playlists

## Base URL
/api/{APP_VERSION}/me/genre-playlists/

## Authentication
JWT token required

## Permissions
Authenticated users only (IsAuthenticated)

## Endpoints
| Method | Path | Action | Description |
|------|------|--------|-------------|
| GET | / | list | List genre playlists |
| GET | /{id}/ | retrieve | Get genre playlist details |

## Request / Response

### GET /

**Description**
List genre playlists

**Request**
Headers:
Authorization: Bearer {token}

Query params:
page, page_size, name, parent

Body:
None

**Response**
Status codes:
 | 00 OK

Body:
```json
{
  "count": 10,
  "next": null,
  "previous": null,
  "results": [
    {
      "uuid": "uuid",
      "name": "string",
      "uploaded_track_playlist_relations": [],
      "uploaded_tracks_count": 10,
      "duration_in_sec": 3600,
      "duration_str_in_hour_min_sec": "1:00:00",
      "uploaded_tracks_archived_count": 0,
      "criteria": {},
      "parent": {},
      "root": {},
      "created_on": "2023-01-01T00:00:00Z",
      "updated_on": "2023-01-01T00:00:00Z"
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
 | 04	Not Found - Playlist not found	

### GET /{id}/

**Description**
Get genre playlist details

**Request**
Headers:
Authorization: Bearer {token}

Query params:
None

Body:
None

**Response**
Status codes:
 | 00 OK

Body:
```json
{
  "uuid": "uuid",
  "name": "string",
  "uploaded_track_playlist_relations": [],
  "uploaded_tracks_count": 10,
  "duration_in_sec": 3600,
  "duration_str_in_hour_min_sec": "1:00:00",
  "uploaded_tracks_archived_count": 0,
  "criteria": {},
  "parent": {},
  "root": {},
  "created_on": "2023-01-01T00:00:00Z",
  "updated_on": "2023-01-01T00:00:00Z"
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
 | 04	Not Found - Playlist not found	

### Versioning

{APP_VERSION}

### Notes
None