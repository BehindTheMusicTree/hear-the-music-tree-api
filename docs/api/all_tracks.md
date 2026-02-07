# all-tracks

## Overview
List all uploaded tracks for the user

## Base URL
/api/{APP_VERSION}/all-tracks/

## Authentication
JWT token required

## Permissions
Authenticated users only (IsAuthenticated)

## Endpoints
| Method | Path | Action | Description |
|------|------|--------|-------------|
| GET | / | list | List all uploaded tracks |

## Request / Response

### GET /

**Description**
List all uploaded tracks for the authenticated user

**Request**
Headers:
Authorization: Bearer {token}

Query params:
page, page_size

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
      "title": "string",
      "artists": []
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

{APP_VERSION}

### Notes
None