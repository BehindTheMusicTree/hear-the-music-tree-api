# users/spotify

## Overview
Manage Spotify user profiles

## Base URL
/api/{APP_VERSION}/users/spotify/

## Authentication
JWT token required

## Permissions
- **List** (`GET /`): Requires app authentication (JWT). Returns 401 if not logged in.
- **Retrieve** (`GET /{id}/`): Requires app authentication and Spotify linked. Returns 401 if not logged in, 403 if logged in but Spotify not linked (code 1005).

## Endpoints
| Method | Path | Action | Description |
|--------|------|--------|-------------|
| GET | / | list | List (current user's Spotify profile only; empty if not Spotify user) |
| GET | /{id}/ | retrieve | Get Spotify user profile for the current user |

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
| 200 | OK |
| 401 | Unauthorized - Not authenticated to the app (code 1006) or invalid/expired token (1001) |
| 403 | Forbidden - Logged in but Spotify not linked (code 1005) |

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
- User must be authenticated to the app (JWT).
- For retrieve (and effectively for list), the user must have completed Spotify OAuth (be a Spotify user); otherwise the API returns 403 with code 1005.

### Errors
| HTTP | API code | details.code | Meaning |
|------|----------|--------------|---------|
| 401 | 1006 | `authentication_required` | Not logged in to the app → redirect to app login |
| 403 | 1005 | `spotify_authorization_required` | Logged in but Spotify not linked → redirect to Spotify OAuth |
| 401 | 1001 | `authentication_failed` / `spotify_authentication_error` | Invalid/expired token or Spotify auth failed |
| 404 | 3001 | `not_found` | User or profile not found |

**Frontend:** See [Authentication and Spotify handling](../frontend/authentication-and-spotify.md) for how to handle 401/403 and these codes.

### Versioning

{APP_VERSION}

### Notes
Only accessible for the current user's own profile