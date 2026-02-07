# playlists

## Overview
Manage playlists

## Base URL
/api/{APP_VERSION}/playlists/

## Authentication
JWT token required

## Permissions
Authenticated users only (IsAuthenticated)

## Endpoints
| Method | Path | Action | Description |
|------|------|--------|-------------|
| GET | / | list | List playlists |
| GET | /{id}/ | retrieve | Get playlist details |

## Request / Response

### GET /

**Description**
List playlists

**Request**
Headers:
Authorization: Bearer {token}

Query params:
page, page_size, name, type

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
      "type": "string",
      "uploaded_tracks_count": 10,
      "uploaded_track_playlist_relations": [],
      "uploaded_tracks_archived_count": 0,
      "duration_in_sec": 3600,
      "duration_str_in_hour_min_sec": "1:00:00",
      "play_count": 0,
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
Get playlist details

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
  "type": "string",
  "uploaded_tracks_count": 10,
  "uploaded_track_playlist_relations": [],
  "uploaded_tracks_archived_count": 0,
      "duration_in_sec": 3600,
      "duration_str_in_hour_min_sec": "1:00:00",
      "play_count": 0,
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