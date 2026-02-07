# users

## Overview
Manage user accounts (admin only)

## Base URL
/api/{APP_VERSION}/users/

## Authentication
JWT token required

## Permissions
Admin users only (IsAdminUser)

## Endpoints
| Method | Path | Action | Description |
|------|------|--------|-------------|
| GET | / | list | List all users |
| GET | /{id}/ | retrieve | Get user details |
| DELETE | /{id}/ | destroy | Delete user |

## Request / Response

### GET /

**Description**
List all users

**Request**
Headers:
Authorization: Bearer {token}

Query params:
page, page_size (pagination)

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
      "id": "uuid",
      "username": "string",
      "email": "string",
      "is_test_user": false,
      "is_staff": false,
      "is_superuser": false,
      "groups": [],
      "user_permissions": []
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
403	Forbidden - Not admin
404	Not Found - User not found	

### GET /{id}/

**Description**
Get user details

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
  "id": "uuid",
  "username": "string",
  "email": "string",
  "is_test_user": false,
  "is_staff": false,
  "is_superuser": false,
  "groups": [],
  "user_permissions": []
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
403	Forbidden - Not admin
404	Not Found - User not found	

### DELETE /{id}/

**Description**
Delete user

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
403	Forbidden - Not admin
404	Not Found - User not found	

Versioning

{APP_VERSION}

Notes
None