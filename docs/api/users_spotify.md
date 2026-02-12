# users/spotify

## Overview
Manage Spotify user profiles

## Base URL
/api/{APP_VERSION}/users/spotify/

## Authentication
JWT token required

## Permissions
Authenticated users only (IsAuthenticated)

## Endpoints
| Method | Path | Action | Description |
|------|------|--------|-------------|
| GET | /{id}/ | retrieve | Get Spotify user profile |

## Request / Response

### GET /{id}/

**Description**
Get the Spotify user profile for the specified user (must be the current user)

**Request**
Headers:
Authorization: Bearer {token}

Query params:
None

Body:
```json
{}
```

**Response**
Status codes:
 | 00 OK

Body:
```json
{
  "spotify_id": "string",
  "email": "string",
  "spotify_profile": {},
  "display_name": "string",
  "followers": {},
  "href": "string",
  "images": [],
  "type": "string",
  "uri": "string",
  "spotify_library_last_synced_at": "2023-01-01T00:00:00Z"
}
```

### Validation Rules
None

### Business Rules
User must have Spotify authorization

### Errors
| Code | Meaning |
|------|----------|
| 400 | Bad Request - Invalid parameters |
| 401 | Unauthorized - Invalid token |
| 403 | Forbidden - User not authorized with Spotify |
| 404 | Not Found - User not found |

### Versioning

{APP_VERSION}

### Notes
Only accessible for the current user's own profile