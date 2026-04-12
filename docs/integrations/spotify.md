# Spotify Data Storage & Compliance Guide

---

# Table of Contents
1. [Overview](#overview)
2. [What Data You May Store](#what-data-you-may-store)
3. [What Data You May Store Temporarily](#what-data-you-may-store-temporarily)
4. [What Data You May NOT Store](#what-data-you-may-not-store)
5. [User Consent Requirements](#user-consent-requirements)
6. [Data Deletion Requirements](#data-deletion-requirements)
7. [Recommended Backend Architecture](#recommended-backend-architecture)
8. [No Shared/System Spotify Account](#no-shared-system-spotify-account)
9. [Official Spotify Documentation Links](#official-spotify-documentation-links)

---

# 1. Overview
Spotify allows backend applications to store certain types of data retrieved through the Spotify Web API. However, Spotify enforces strict rules regarding user privacy, data retention, and scope‑based access.

This document summarizes what your backend may store, what it must delete, and how to remain compliant with Spotify’s Developer Terms and Policy.

---

# 2. What Data You May Store
These types of data are safe to store long‑term because they are public or non‑sensitive:

### ✔ Public or Semi‑Public Data
- Track IDs and metadata
- Album IDs and metadata
- Artist IDs and metadata
- Playlist IDs (public playlists)
- Audio features (danceability, energy, etc.)
- Audio analysis
- Search results
- Public user profile info (display name, profile image, country if provided)

**Why allowed:**
Spotify’s policies focus on protecting user‑specific private data, not public catalog data.

---

# 3. What Data You May Store Temporarily
These require ongoing user consent and regular refresh:

### ⚠️ Temporarily allowed:
- Access tokens (short‑lived)
- Refresh tokens (long‑lived)
- User’s private playlists
- User’s saved tracks
- User’s library data
- User’s listening history (recently played)

### Requirements
- Must be refreshed at least every **30 days**
- Must be deleted if the user revokes access
- Must only be used for the scopes the user approved

---

# 4. What Data You May NOT Store
Spotify forbids storing certain sensitive or personal data:

### ❌ Forbidden:
- User passwords
- Email addresses (unless user explicitly grants `user-read-email`)
- Long‑term storage of listening history
- Any data after a user disconnects your app
- Any data not covered by granted scopes

---

# 5. User Consent Requirements
Spotify requires:

### ✔ Explicit user authorization
Your app may only access and store data for scopes the user approved during OAuth.

### ✔ Transparency
You must clearly explain:
- What data you collect
- Why you collect it
- How long you store it

### ✔ Respect for user privacy settings
If a user changes their Spotify privacy settings, your app must comply.

---

# 6. Data Deletion Requirements
Your backend must delete:

### ✔ All user‑specific data if:
- The user revokes access
- You stop refreshing the data
- The user requests deletion

### ✔ All sensitive data after 30 days if not refreshed
Spotify requires periodic refresh to ensure data accuracy and user consent.

---

# 7. Recommended Backend Architecture

### **Database should store:**
- `spotify_user_id`
- `refresh_token`
- `access_token` (short‑lived)
- Cached playlist/track data
- App‑specific metadata (preferences, settings)

### **Do NOT store:**
- Sensitive personal data
- Anything outside granted scopes
- Long‑term listening history

### **Flow**
1. User logs in via Spotify OAuth
2. Backend stores refresh token + user ID
3. Backend fetches data as needed
4. Backend refreshes tokens and data periodically
5. Backend deletes data if user disconnects

---

# 8. No Shared/System Spotify Account

To comply with Spotify’s [User Guidelines](https://www.spotify.com/legal/user-guidelines) and [Developer Policy](https://developer.spotify.com/policy):

- **One account per user.** You must not use a single “system” or “reference” Spotify account whose library or data is exposed to or shared with all users of your application. That would constitute account sharing.
- **Per-user linking.** Each end user must link their own Spotify account via OAuth (Authorization Code flow). Your app must use that user’s tokens only for that user and must allow them to disconnect at any time.
- **No reference Spotify library.** This API does not expose a shared “reference” Spotify library endpoint. Only the authenticated user’s own library is available under `me/library/spotify/`. Other reference endpoints (e.g. reference albums, genres, uploaded tracks) use app-owned data, not a shared Spotify account.

---

# 9. Official Spotify Documentation Links

### Spotify Developer Terms
https://developer.spotify.com/terms

### Spotify Developer Policy
https://developer.spotify.com/policy

### Spotify Web API Reference
https://developer.spotify.com/documentation/web-api

### Authorization Guide
https://developer.spotify.com/documentation/web-api/tutorials/code-flow

### User Data & Scopes
https://developer.spotify.com/documentation/web-api/concepts/scopes
