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
| POST | / | create | Create a new genre |
| GET | /{id}/ | retrieve | Get genre details |
| PUT | /{id}/ | update | Update genre |
| DELETE | /{id}/ | destroy | Delete genre |
| GET | /tree/ | tree | Get genres tree |
| POST | /tree/import/ | import_tree | Import genres tree |

## Request / Response

### GET /

**Description**
List genres

**Request**
Headers:
None

Query params:
page, page_size, name, parent

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
}
```

### Validation Rules
None

### Business Rules
Returns only genres owned by the system user (TMTA_USERNAME)

### Errors
| Code | Meaning |
|------|---------|
| 400 | Bad Request - Invalid parameters |
| 404 | Not Found |

### POST /

**Description**
Create a new genre

**Request**
Headers:
None

Query params:
None

Body:
```json
{
  "name": "string",
  "parent": "uuid"
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
```

### Validation Rules
Name required, max length

### Business Rules
None

### Errors
| Code | Meaning |
|------|---------|
| 400 | Bad Request - Invalid parameters |

### GET /{id}/

**Description**
Get genre details

**Request**
Headers:
None

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
```

### Validation Rules
None

### Business Rules
None

### Errors
| Code | Meaning |
|------|---------|
| 400 | Bad Request - Invalid parameters |
| 404 | Not Found - Genre not found |

### PUT /{id}/

**Description**
Update genre

**Request**
Headers:
None

Query params:
None

Body:
```json
{
  "name": "string",
  "parent": "uuid"
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
```

### Validation Rules
Name max length

### Business Rules
None

### Errors
| Code | Meaning |
|------|---------|
| 400 | Bad Request - Invalid parameters |
| 404 | Not Found - Genre not found |

### DELETE /{id}/

**Description**
Delete genre

**Request**
Headers:
None

Query params:
None

Body:
None

**Response**
Status codes:
204 No Content

Body:
None

### Validation Rules
None

### Business Rules
Children reassigned to parent

### Errors
| Code | Meaning |
|------|---------|
| 400 | Bad Request - Invalid parameters |
| 404 | Not Found - Genre not found |

### GET /tree/

**Description**
Get genres tree

**Request**
Headers:
None

Query params:
None

Body:
None

**Response**
Status codes:
200 OK

Body:
```json
[
  {
    "name": "string",
    "children": []
  }
]
```

### Validation Rules
None

### Business Rules
None

### Errors
| Code | Meaning |
|------|---------|
| None | None |

### POST /tree/import/

**Description**
Import genres tree

**Request**
Headers:
None

Query params:
None

Body:
```json
[
  {
    "name": "string",
    "children": []
  }
]
```

**Response**
Status codes:
201 Created

Body:
```json
{
  "count": 10,
  "next": null,
  "previous": null,
  "results": []
}
```

### Validation Rules
None

### Business Rules
Replaces all existing genres

### Errors
| Code | Meaning |
|------|---------|
| 400 | Bad Request - Invalid parameters |

### Versioning

{APP_VERSION}

### Notes
This endpoint is public and does not require authentication. It provides reference genres for public consumption.
