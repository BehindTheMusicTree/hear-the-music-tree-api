# tags

## Overview
Manage tags

## Base URL
/api/{APP_VERSION}/tags/

## Authentication
JWT token required

## Permissions
Authenticated users only (IsAuthenticated)

## Endpoints
| Method | Path | Action | Description |
|------|------|--------|-------------|
| GET | / | list | List tags |
| POST | / | create | Create a new tag |
| GET | /{id}/ | retrieve | Get tag details |
| PUT | /{id}/ | update | Update tag |
| DELETE | /{id}/ | destroy | Delete tag |
| GET | /tree/ | tree | Get tags tree |
| POST | /tree/import/ | import_tree | Import tags tree |

## Request / Response

### GET /

**Description**
List tags

**Request**
Headers:
Authorization: Bearer {token}

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

Validation Rules
None

Business Rules
None

Errors
Code	Meaning
400	Bad Request - Invalid parameters
401	Unauthorized - Invalid token
404	Not Found - Tag not found	

### POST /

**Description**
Create a new tag

**Request**
Headers:
Authorization: Bearer {token}

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
Get tag details

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

Validation Rules
None

Business Rules
None

Errors
Code	Meaning
400	Bad Request - Invalid parameters
401	Unauthorized - Invalid token
404	Not Found - Tag not found	

### PUT /{id}/

**Description**
Update tag

**Request**
Headers:
Authorization: Bearer {token}

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

Validation Rules
Name max length

Business Rules
None

Errors
Code	Meaning
400	Bad Request - Invalid parameters
401	Unauthorized - Invalid token
404	Not Found - Tag not found	

### DELETE /{id}/

**Description**
Delete tag

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
Children reassigned to parent

Errors
Code	Meaning
400	Bad Request - Invalid parameters
401	Unauthorized - Invalid token
404	Not Found - Tag not found	

### GET /tree/

**Description**
Get tags tree

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
[
  {
    "name": "string",
    "children": []
  }
]
```

Validation Rules
None

Business Rules
None

Errors
Code	Meaning
401	Unauthorized - Invalid token	

### POST /tree/import/

**Description**
Import tags tree

**Request**
Headers:
Authorization: Bearer {token}

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

Validation Rules
None

Business Rules
Replaces all existing tags

Errors
Code	Meaning
400	Bad Request - Invalid parameters
401	Unauthorized - Invalid token	

Versioning

{APP_VERSION}

Notes
None