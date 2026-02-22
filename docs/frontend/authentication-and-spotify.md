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
| **401** | **1007** | `spotify_user_not_allowlisted` | Spotify app is in development mode; this user is not in the app's User Management. | Show `details.message`; user cannot sign in until the app owner adds them in the Spotify Developer Dashboard. |
| **401** | **1008** | `spotify_code_expired_or_used` | Authorization code expired or already used (e.g. code sent twice, or too slow). | Show `details.message`; suggest starting the Spotify connect flow again (and send the code only once). |
| **401** | **1001** | `spotify_authentication_error` | Other Spotify login/callback failure (e.g. user denied, invalid code). | Show `details.message`; optionally retry or open Spotify app/settings. |
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
   - **401** and **`code === 1007`** (or `details.code === 'spotify_user_not_allowlisted'`):
     - User not in Spotify app's allowlist (development mode) → show `details.message`; user cannot complete sign-in until added in the dashboard.
   - **401** and **`code === 1001`**:
     - Invalid/expired token or other Spotify auth error → clear tokens and redirect to app login, or show `details.message` for Spotify-specific errors.

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

if (response.status === 401 && (apiCode === 1007 || detailsCode === 'spotify_user_not_allowlisted')) {
  // User not in Spotify app allowlist (dev mode)
  showError(err.details?.message ?? err.message);
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
- **401 + 1007** → User not in Spotify app allowlist (dev mode) → show message.
- **401 + 1001** → Bad/expired token or other Spotify auth failure → **app login** or show message.

---

## Spotify allowlist (development mode) — how the API handles it

When the Spotify app is in **development mode**, only Spotify accounts that the app owner has added in the [Spotify Developer Dashboard](https://developer.spotify.com/dashboard) (Settings → User Management) can complete sign-in. Any other user can go through the OAuth flow (authorize on Spotify, redirect back with a code), but when the API then calls Spotify (e.g. to get the user profile), Spotify returns **403** and the sign-in fails.

### What the API does

1. The frontend sends the authorization `code` to `POST /api/{version}/auth/spotify/`.
2. The API exchanges the code for tokens with Spotify (this can succeed).
3. The API calls Spotify’s `GET /v1/me` to fetch the user profile. If the user is **not** in the app’s User Management list, Spotify responds with **403** and a message like “Check settings on developer.spotify.com/dashboard, the user may not be registered.”
4. The API **does not** return 500 or the raw Spotify error. It:
   - Returns **401 Unauthorized**.
   - Sets **`code`** to **1007** and **`details.code`** to **`spotify_user_not_allowlisted`**.
   - Sets **`details.message`** to a user-facing message, e.g. *“Spotify app is in development mode. Your account must be added in the Spotify Developer Dashboard (Users and Access) to sign in.”*

So the frontend can rely on **401 + code 1007** (or `details.code === 'spotify_user_not_allowlisted'`) to detect this case and show a specific UI without parsing the message text.

### What the frontend should do

- **Detect:** On `POST /auth/spotify/` (or any Spotify auth callback), if the response is **401** and **`code === 1007`** or **`details.code === 'spotify_user_not_allowlisted'`**, treat it as "user not allowlisted."
- **Show:** Display **`details.message`** to the user (and optionally a short note that the app is in testing mode and they need to ask the app owner to add their Spotify account).
- **Do not:** Do not redirect again to Spotify OAuth or suggest "try again" without explaining that they must be added in the dashboard first; retrying will produce the same result until the app owner adds them or the app is moved to Extended Quota Mode.

The app owner can add up to 5 users in Dashboard → App → Settings → User Management. Once the app is in **Extended Quota Mode** (non–dev mode), the allowlist is no longer used and this error no longer occurs for that app.

---

## "Invalid authorization code" (401, spotify_authentication_error)

When exchanging the OAuth code with `POST /auth/spotify/`, Spotify may return **invalid_grant** ("Invalid authorization code"). The API turns this into **401** with `details.code === 'spotify_authentication_error'` and a message like *"Authorization code expired or already used. Please try connecting with Spotify again."*

Common causes:

1. **Code already used** – Authorization codes are **single-use**. If the frontend sends the same code twice (e.g. double submit, retry, or two components both calling the backend), the first exchange succeeds and the second fails. **Fix:** Send the code only once (e.g. clear it from URL/state after the first request, or disable the submit button until the request completes).
2. **Redirect URI mismatch** – The `redirect_uri` used when exchanging the code must match **exactly** what was used in the authorization request (including scheme, host, port, path, trailing slashes). **Fix:** Ensure the backend `SPOTIFY_REDIRECT_URI` matches the redirect URI configured in the Spotify Dashboard and used when opening the Spotify auth URL.
3. **Code expired** – Codes typically expire after about 60 seconds. **Fix:** User starts the Spotify connect flow again.
