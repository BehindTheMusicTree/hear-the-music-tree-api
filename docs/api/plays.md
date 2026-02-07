# plays

## Overview
Manage play history

## Base URL
/api/{APP_VERSION}/plays/

## Authentication
JWT token required

## Permissions
Authenticated users only (IsAuthenticated)

## Endpoints
| Method | Path | Action | Description |
|------|------|--------|-------------|
| GET | / | list | List plays |
| POST | / | create | Record a new play |
| GET | /{id}/ | retrieve | Get play details |

## Request / Response

### GET /

**Description**
List plays

**Request**
Headers:
Authorization: Bearer {token}

Query params:
page, page_size

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
      "content_type": "string",
      "content": {},
      "created_on": "2023-01-01T00:00:00Z"
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
404	Not Found - Play not found	

### POST /

**Description**
Record a new play

**Request**
Headers:
Authorization: Bearer {token}

Query params:
None

Body:
```json
{
  "content": "uuid"
}
```

**Response**
Status codes:
201 Created

Body:
```json
{
  "uuid": "uuid",
  "content_type": "string",
  "content": {},
  "created_on": "2023-01-01T00:00:00Z"
}
```

Validation Rules
Content required, must be valid uuid of track or playlist

Business Rules
None

Errors
Code	Meaning
400	Bad Request - Invalid parameters
401	Unauthorized - Invalid token	

### GET /{id}/

**Description**
Get play details

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
  "content_type": "string",
  "content": {},
  "created_on": "2023-01-01T00:00:00Z"
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
404	Not Found - Play not found	

Versioning

{APP_VERSION}

Notes
None