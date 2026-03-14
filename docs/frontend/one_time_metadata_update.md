# Frontend: Metadata session (no auth)

This document describes how to implement the **metadata session** flow in the frontend: upload a file, show/edit metadata, then download the file with updated tags. No user account is required.

## Flow overview

1. **Upload** — User selects an audio file (or enters a URL). Frontend sends it to the API and receives **metadata** plus a **session token**.
2. **Edit** — User sees the metadata (and optional MusicBrainz data) and can edit fields (title, artists, album, etc.) in the UI.
3. **Download** — User clicks “Download”. Frontend sends the **session token** and the **current metadata** to the API and receives the **file** with those tags written in. This step can be repeated (e.g. user changes metadata again and downloads again) until the session expires (15 minutes).

## API endpoints

Base URL is your API root (e.g. `https://api.example.com/v1`).

### Step 1: Create session (upload)

- **Method**: `POST`
- **URL**: `/v1/audio/metadata/session/`
- **Request**:
  - **Option A (file upload)**  
    - `Content-Type: multipart/form-data`  
    - Body: `file` = the audio file (required)  
    - Optional: `include_musicbrainz_analysis` = `true` to get MusicBrainz lookup in the response
  - **Option B (URL)**  
    - `Content-Type: application/json`  
    - Body: `{ "file": "https://example.com/audio.mp3", "include_musicbrainz_analysis": false }`
- **Response**: `200 OK`, JSON. Same shape as the full metadata endpoint (`POST /v1/audio/metadata/full/`), plus:
  - `sessionToken` (or `session_token` depending on your API’s response casing)
  - `sessionExpiresInSeconds` (or `session_expires_in_seconds`) = `900` (15 minutes)

**Example (multipart with fetch)**:

```javascript
const formData = new FormData();
formData.append("file", audioFile);
formData.append("include_musicbrainz_analysis", "true");

const response = await fetch("/v1/audio/metadata/session/", {
  method: "POST",
  body: formData,
});
const data = await response.json();
const sessionToken = data.sessionToken ?? data.session_token;
const expiresIn = data.sessionExpiresInSeconds ?? data.session_expires_in_seconds;
// Store sessionToken; use it for download. Optionally show a countdown for expiresIn.
```

**Example (camelCase response)**  
If your API returns camelCase (e.g. `sessionToken`, `sessionExpiresInSeconds`), use those keys. If it returns snake_case (`session_token`, `session_expires_in_seconds`), use those. Handle both for robustness.

### Step 2: Download (apply metadata and get file)

- **Method**: `POST`
- **URL**: `/v1/audio/metadata/session-download/`
- **Request**:
  - **Session token** (required): send either
    - Header: `X-Session-Token: <sessionToken>`
    - Or in JSON body: `session_token: "<sessionToken>"`
  - **Metadata (optional)** — JSON body with any of: `title`, `artists_names`, `album_name`, `album_artists_names`, `genres_names` (list of strings), `rating`, `language`. Only provided fields are written; omit a field to leave it unchanged. To get the file as-is, send an empty object `{}` but still send the token (e.g. in the header).
- **Response**:
  - `200 OK`: Body is the **binary audio file**. Response header `Content-Disposition: attachment; filename="..."` gives the suggested filename.
  - `400 Bad Request`: Missing session token.
  - `410 Gone`: Session expired or invalid. Prompt the user to upload again.

**Example (token in header, metadata in body)**:

```javascript
const response = await fetch("/v1/audio/metadata/session-download/", {
  method: "POST",
  headers: {
    "Content-Type": "application/json",
    "X-Session-Token": sessionToken,
  },
  body: JSON.stringify({
    title: editedTitle,
    artists_names: editedArtists,
    album_name: editedAlbum,
    // ... other fields the user edited
  }),
});

if (response.status === 410) {
  // Session expired; ask user to upload again
  return;
}
if (!response.ok) {
  // Handle 400 etc.
  return;
}

const blob = await response.blob();
const filename = response.headers.get("Content-Disposition")?.match(/filename="(.+)"/)?.[1] ?? "download.mp3";
// Trigger download: e.g. create object URL and <a download>
const url = URL.createObjectURL(blob);
const a = document.createElement("a");
a.href = url;
a.download = filename;
a.click();
URL.revokeObjectURL(url);
```

## UI/UX suggestions

- **After upload**: Show the returned metadata in editable fields. Optionally show MusicBrainz data (e.g. `musicbrainz_raw_data`) so the user can copy or merge.
- **Session expiry**: Show a short message like “Session expires in 15 minutes” or a countdown. If the user tries to download and gets `410`, show “Session expired. Please upload the file again.”
- **Multiple downloads**: Allow “Download” every time the user changes metadata; no need to re-upload. Each request can send the same token with the new metadata.
- **Empty metadata**: If the user does not change anything, you can still call download with an empty body `{}` (and the token in the header) to get the original file.

## Field names

Use the same field names as in the upload response (and full-metadata API):

- `title` (string)
- `artists_names` (array of strings)
- `album_name` (string)
- `album_artists_names` (array of strings)
- `genre_name` (string)
- `rating` (integer, 0–100 or format-dependent)
- `language` (string)

Send only the fields you want to write; omit others to leave them unchanged.

## Errors

| Status | Meaning |
|--------|--------|
| 400 | Bad request (e.g. missing file, invalid format, or missing session token on download). |
| 410 | Session not found or expired. User should create a new session (upload again). |
| 413 | File too large. |

## Summary

- **Upload** → `POST /v1/audio/metadata/session/` with file (or URL) → store `sessionToken`, show metadata.
- **Download** → `POST /v1/audio/metadata/session-download/` with `X-Session-Token` (or `session_token` in body) + optional metadata JSON → receive file, trigger download. Repeat as needed until the session expires (15 minutes).
