# Frontend: Handling authentication and Spotify errors

Use this guide when calling endpoints that require app login and/or Spotify (e.g. `GET /v1/me/spotify/`, Spotify library, etc.). The API path uses the major version only (e.g. `v1`).

## Error response shape

All error responses use this structure:

```json
{
  "code": 1006,
  "message": "Unauthorized",
  "success": false,
  "details": {
    "message": "Authentication required",
    "code": "authentication_required"
  }
}
```

- **`code`** (number): API error code (1001, 1005, 1006, etc.).
- **`details.code`** (string): Machine-readable key for the specific case.
- **`details.message`** (string): Human-readable message.

## HTTP status and API codes

| HTTP status | API `code` | `details.code` | Meaning | Frontend action |
|-------------|------------|----------------|---------|-----------------|
| **401** | **1006** | `authentication_required` | User is **not logged in** to the app. | Redirect to **app login** (e.g. login page or token obtain). Do **not** redirect to Spotify. |
| **403** | **1005** | `spotify_authorization_required` | User **is logged in** to the app but has **not linked Spotify**. | Show “Connect Spotify” / “Link Spotify” and redirect to **Spotify OAuth** (e.g. open auth URL from your backend or start your Spotify connect flow). |
| **401** | **1001** | `spotify_authentication_error` | Spotify login/callback failed (e.g. user denied, app in dev mode). | Show error from `details.message`; optionally retry or open Spotify app/settings. |
| **401** | **1001** | `authentication_failed` | Invalid or expired JWT. | Clear stored tokens and redirect to **app login**. |

## Recommended flow

1. **On request to a Spotify-required endpoint** (e.g. `GET /me/spotify/` or list):
   - Send the request with the app’s JWT (e.g. `Authorization: Bearer <access_token>`).

2. **On response:**
   - **200** → Success; use the payload.
   - **401** and **`code === 1006`** (or `details.code === 'authentication_required'`):
     - User is not logged in to the app → redirect to **app login**.
   - **403** and **`code === 1005`** (or `details.code === 'spotify_authorization_required'`):
     - User is logged in but Spotify not linked → show “Connect Spotify” and start **Spotify OAuth** (do not log the user out of the app).
   - **401** and **`code === 1001`**:
     - Invalid/expired token or Spotify auth error → clear tokens and redirect to app login, or show `details.message` for Spotify-specific errors.

## Example (pseudo-code)

```javascript
const response = await fetch('/v1/me/spotify/', {
  headers: { Authorization: `Bearer ${appAccessToken}` }
});

if (response.ok) {
  const data = await response.json();
  // use data
  return;
}

const err = await response.json();
const apiCode = err.code;
const detailsCode = err.details?.code;

if (response.status === 401 && (apiCode === 1006 || detailsCode === 'authentication_required')) {
  // Not logged in to the app → app login
  redirectToAppLogin();
  return;
}

if (response.status === 403 && (apiCode === 1005 || detailsCode === 'spotify_authorization_required')) {
  // Logged in but Spotify not linked → Spotify OAuth
  redirectToSpotifyConnect();
  return;
}

if (response.status === 401 && apiCode === 1001) {
  // Invalid token or Spotify error
  clearTokens();
  redirectToAppLogin();
  return;
}

// Other errors: show err.details?.message or err.message
showError(err.details?.message ?? err.message);
```

## Summary

- **401 + 1006** → Not logged in to the app → **app login**.
- **403 + 1005** → Logged in, Spotify not linked → **Connect Spotify** (Spotify OAuth).
- **401 + 1001** → Bad/expired token or Spotify auth failure → **app login** or show message.
