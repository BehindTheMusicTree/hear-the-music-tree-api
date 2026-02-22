# Frontend: Unified account (Google + Spotify) and linking

One user account can sign in with **Google**, **Spotify**, or both. The backend links providers by **email**: if the user signs in with a new provider and their email matches an existing account, that provider is linked to the same account.

## How the backend handles unified auth

### Endpoints (no auth required)

| Action | Endpoint | Body | Response |
|--------|----------|------|----------|
| Exchange Google code for session | `POST /v1/auth/google/` | `{ "code": "<authorization_code>" }` | Session (see below) |
| Exchange Spotify code for session | `POST /v1/auth/spotify/` | `{ "code": "<authorization_code>" }` | Session + optional `spotifyUser` |

### Session response shape

- **Google**: `{ "accessToken", "refreshToken", "expiresAt" }`.
- **Spotify**: same three fields, plus `spotifyUser` (current user’s Spotify profile and app user id, email, etc.).

The same JWT is used for all API calls regardless of sign-in method. Use `Authorization: Bearer <accessToken>`.

### Backend logic (create vs link)

- **Lookup by provider id**: If a user already exists with this `google_id` or `spotify_id`, the backend **updates** that user’s tokens/profile and returns a session (same account).
- **Lookup by email (linking)**: If no user with that provider id exists but the provider returned an **email**, the backend looks up by `email` (case-insensitive). If found, it **links** the new provider to that user (sets `google_id`/`spotify_id` and tokens) and returns a session. No second account is created.
- **New user**: If neither provider id nor email matches, the backend **creates** a new user with that provider’s id, email, and tokens.

So the frontend always receives one session per “person”; the backend decides create vs link by provider id and email.

### Auth error response shape

On failure, auth endpoints return **401 Unauthorized** (or 500 for misconfiguration) with a body like:

```json
{
  "code": 1001,
  "message": "Unauthorized",
  "success": false,
  "details": {
    "message": "Human-readable message",
    "code": "detail_code"
  }
}
```

Use **`details.code`** to choose the right message or flow.

### Spotify auth `details.code` values

| `details.code` | Meaning | Suggested frontend action |
|----------------|---------|---------------------------|
| `spotify_authentication_error` | Generic Spotify auth failure (e.g. user denied, invalid/expired code). | Show `details.message`; retry or redirect to app login. |
| `spotify_user_not_in_allowlist` | App is in Development Mode and this user is not in the Spotify app allowlist. | Show: “Your Spotify account is not authorized for this app. The app owner must add you in the Spotify Developer Dashboard (User Management).” Do not treat as generic login failure. |

### Google auth `details.code` values

| `details.code` | Meaning | Suggested frontend action |
|----------------|---------|---------------------------|
| `google_authentication_error` | Generic Google auth failure. | Show `details.message`; retry or redirect to app login. |
| `google_oauth_code_invalid_or_expired` | Code already used or expired. | Ask user to sign in with Google again. |
| `google_oauth_redirect_uri_mismatch` | Redirect URI does not match Google Console. | Show: “Sign-in is temporarily misconfigured. Please try again later or contact support.” (Backend may return 500.) |
| `google_oauth_invalid_client` | Client id/secret misconfigured. | Same as above. |

### Checking if Spotify is linked

- **`GET /v1/me/spotify/`** with the app JWT:
  - **200** and non-empty list → Spotify is linked; use the payload for profile.
  - **403** with `details.code === 'spotify_authorization_required'` → User is logged in but Spotify is not linked; show “Connect Spotify” and start Spotify OAuth.

Google linked state is not exposed by a dedicated endpoint; it can be inferred from how the user signed in or a future “linked providers” API.

## How the frontend should handle it

### 1. One session type

- Store **one** session shape for both Google and Spotify sign-in: `accessToken`, `refreshToken`, `expiresAt`.
- Use the same token for all API calls regardless of how the user signed in (Google, Spotify, or both).

### 2. Login options

- Offer **Sign in with Google** and **Sign in with Spotify** (and any future providers).
- After redirect from the provider, send the **authorization code** to the correct backend endpoint:
  - Google → `POST /v1/auth/google/` with `{ "code": "..." }`
  - Spotify → `POST /v1/auth/spotify/` with `{ "code": "..." }`
- Store the returned `accessToken` / `refreshToken` / `expiresAt` the same way for both.

### 3. No “choose account” needed for linking

- You do **not** need to ask “Link to existing account?”. The backend links by email automatically when it matches.
- If the same email is used for Google and Spotify, the user will have one account with both providers linked after signing in with each once.

### 4. Optional: show linked providers

- To show “Connected with Google” / “Connected with Spotify”, use:
  - **Spotify**: `GET /me/spotify/`. If **200** and non-empty, Spotify is linked. If **403** with `spotify_authorization_required`, Spotify is not linked.
  - **Google**: There is no separate “me/google” endpoint today; the backend does not expose a Google profile in the same way. You can infer “signed in with Google” from the fact that the user obtained the session via `POST auth/google/`. For “is Google linked?”, the frontend can track this at login time or the backend could add a small “linked providers” endpoint later.

### 5. Optional: link another provider later

- If the user signed in with Google and later wants to add Spotify:
  - Redirect to Spotify OAuth (same flow as “Sign in with Spotify”).
  - On callback, send the code to `POST auth/spotify/`. The backend will link Spotify to the existing user by email and return the same session (same `accessToken`, etc.).
- Similarly, a user who signed in with Spotify can “add Google” by going through Google OAuth and `POST auth/google/`; the backend links by email.

### 6. Error handling

- On `POST auth/google/` or `POST auth/spotify/` failure: response is **401** (or **500** for some Google misconfig). Read **`details.code`** and **`details.message`** (see tables above) to show the right message or retry.
- For **Spotify-required** endpoints (e.g. `GET /me/spotify/`, library): see `docs/frontend/authentication-and-spotify.md` for 401 vs 403 and `spotify_authorization_required`.

## Summary

| Frontend concern | Behavior |
|------------------|----------|
| Session storage | One format for both Google and Spotify: `accessToken`, `refreshToken`, `expiresAt`. |
| Linking | Automatic by email; no extra UI required. |
| “Link Spotify” / “Link Google” | Same as “Sign in with Spotify” / “Sign in with Google”; backend links if email matches. |
| Checking if Spotify is linked | `GET /me/spotify/` → 200 = linked, 403 = not linked. |
| Checking if Google is linked | Not exposed via a dedicated endpoint; can be inferred from login method or a future “linked providers” API. |
