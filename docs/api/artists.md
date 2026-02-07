# artists

## Overview
Manage artists

## Base URL
/api/{APP_VERSION}/artists/

## Authentication
JWT token required

## Permissions
Authenticated users only (IsAuthenticated)

## Endpoints
| Method | Path | Action | Description |
|------|------|--------|-------------|
| GET | / | list | List artists |
| GET | /{id}/ | retrieve | Get artist details |
| DELETE | /{id}/ | destroy | Delete artist |

## Request / Response

### GET /

**Description**
List artists

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
      "albums": [],
      "uploaded_tracks": [],
      "uploaded_tracks_count": 10,
      "duration_in_sec": 3600,
      "duration_str_in_hour_min_sec": "1:00:00",
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
404	Not Found - Artist not found	

### GET /{id}/

**Description**
Get artist details

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
  "albums": [],
  "uploaded_tracks": [],
  "uploaded_tracks_count": 10,
  "duration_in_sec": 3600,
  "duration_str_in_hour_min_sec": "1:00:00",
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
404	Not Found - Artist not found	

### DELETE /{id}/

**Description**
Delete artist

**Request**
Headers:
Authorization: Bearer {token}

Query params:
None

Body:
None

**Response**
Status codes:
204 No Content

Body:
None

Validation Rules
None

Business Rules
None

Errors
Code	Meaning
400	Bad Request - Invalid parameters
401	Unauthorized - Invalid token
404	Not Found - Artist not found	

Versioning

{APP_VERSION}

Notes
None