# manual-playlists

## Overview
Manage manual playlists

## Base URL
/api/{APP_VERSION}/manual-playlists/

## Authentication
JWT token required

## Permissions
Authenticated users only (IsAuthenticated)

## Endpoints
| Method | Path | Action | Description |
|------|------|--------|-------------|
| GET | / | list | List manual playlists |
| POST | / | create | Create a new manual playlist |
| GET | /{id}/ | retrieve | Get manual playlist details |
| PUT | /{id}/ | update | Update manual playlist |

## Request / Response

### GET /

**Description**
List manual playlists

**Request**
Headers:
Authorization: Bearer {token}

Query params:
page, page_size, name

Body:
None

**Response**
Status codes:
200 OK

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
      "uploaded_tracks": [],
      "uploaded_tracks_count": 10,
      "uploaded_tracks_archived_count": 0,
      "created_on": "2023-01-01T00:00:00Z",
      "updated_on": "2023-01-01T00:00:00Z"
    }
  ]
}
```

Validation Rules
None

Business Rules
None

Errors
Code	Meaning
400	Bad Request - Invalid parameters
401	Unauthorized - Invalid token
404	Not Found - Playlist not found	

### POST /

**Description**
Create a new manual playlist

**Request**
Headers:
Authorization: Bearer {token}

Query params:
None

Body:
```json
{
  "name": "string"
}
```

**Response**
Status codes:
201 Created

Body:
```json
{
  "uuid": "uuid",
  "name": "string",
  "uploaded_tracks": [],
  "uploaded_tracks_count": 10,
  "uploaded_tracks_archived_count": 0,
  "created_on": "2023-01-01T00:00:00Z",
  "updated_on": "2023-01-01T00:00:00Z"
}
```

Validation Rules
Name required, max length

Business Rules
None

Errors
Code	Meaning
400	Bad Request - Invalid parameters
401	Unauthorized - Invalid token	

### GET /{id}/

**Description**
Get manual playlist details

**Request**
Headers:
Authorization: Bearer {token}

Query params:
None

Body:
None

**Response**
Status codes:
200 OK

Body:
```json
{
  "uuid": "uuid",
  "name": "string",
  "uploaded_tracks": [],
  "uploaded_tracks_count": 10,
  "uploaded_tracks_archived_count": 0,
  "created_on": "2023-01-01T00:00:00Z",
  "updated_on": "2023-01-01T00:00:00Z"
}
```

Validation Rules
None

Business Rules
None

Errors
Code	Meaning
400	Bad Request - Invalid parameters
401	Unauthorized - Invalid token
404	Not Found - Playlist not found	

### PUT /{id}/

**Description**
Update manual playlist

**Request**
Headers:
Authorization: Bearer {token}

Query params:
None

Body:
```json
{
  "name": "string"
}
```

**Response**
Status codes:
200 OK

Body:
```json
{
  "uuid": "uuid",
  "name": "string",
  "uploaded_tracks": [],
  "uploaded_tracks_count": 10,
  "uploaded_tracks_archived_count": 0,
  "created_on": "2023-01-01T00:00:00Z",
  "updated_on": "2023-01-01T00:00:00Z"
}
```

Validation Rules
Name max length

Business Rules
None

Errors
Code	Meaning
400	Bad Request - Invalid parameters
401	Unauthorized - Invalid token
404	Not Found - Playlist not found	

Versioning

{APP_VERSION}

Notes
None