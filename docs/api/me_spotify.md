# me/spotify

## Overview
Get the current user's Spotify profile. Only one endpoint: list returns 0 or 1 item.

## Base URL
/v1/me/spotify/

## Authentication
JWT token required

## Permissions
- **List** (`GET /`): Requires app authentication (JWT). Returns 401 if not logged in. Returns 403 if logged in but Spotify not linked (code 1005). Returns paginated list of 0 or 1 item (current user's Spotify profile).

## Endpoints
| Method | Path | Description |
|--------|------|--------------|
| GET | / | Get current user's Spotify profile (list of 0 or 1 item) |

`GET /{id}/` is not supported; use `GET /` instead.

## Request / Response

### GET /

**Description**
Get the current user's Spotify profile. Returns a paginated list containing either 0 items (user not linked to Spotify) or 1 item (current user's Spotify profile).

**Request**
Headers:
Authorization: Bearer {token}

Query params:
Standard list params (page, page_size) if applicable.

Body:
None

**Response**
Status codes:
| 200 | OK |
| 401 | Unauthorized - Not authenticated to the app (code 1006) or invalid/expired token (1001) |
| 403 | Forbidden - Logged in but Spotify not linked (code 1005) |

Body (200, one profile):
```json
{
  "count": 1,
  "next": null,
  "previous": null,
  "results": [
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
  ]
}
```

### Business Rules
- User must be authenticated to the app (JWT).
- User must have completed Spotify OAuth (be a Spotify user) to get a non-empty result; otherwise the API returns 403 with code 1005.

### Errors
| HTTP | API code | details.code | Meaning |
|------|----------|--------------|---------|
| 401 | 1006 | `authentication_required` | Not logged in to the app → redirect to app login |
| 403 | 1005 | `spotify_authorization_required` | Logged in but Spotify not linked → redirect to Spotify OAuth |
| 401 | 1001 | `authentication_failed` / `spotify_authentication_error` | Invalid/expired token or Spotify auth failed |
| 405 | - | - | GET /{id}/ is not supported; use GET / |

**Frontend:** See [Authentication and Spotify handling](../frontend/authentication-and-spotify.md) for how to handle 401/403 and these codes.

### Versioning

API path prefix uses the major version only (e.g. `v1`), derived from `APP_VERSION`.

### Notes
Only the current user's own profile is accessible. Retrieve by id is not provided; use list.
