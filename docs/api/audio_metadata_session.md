# Metadata session (session + download)

## Overview

Public, two-step flow for users who are not authenticated: (1) upload an audio file and get back metadata plus a **session token**; (2) send the token and optional metadata to **download** the same file with tags written in. The session is valid **15 minutes** and is **multi-use**: you can call the download endpoint multiple times with different metadata until the session expires.

No account is required; no data is persisted beyond the 15-minute session.

## Base URLs

- Create session: `/v1/audio/metadata/session/`
- Download: `/v1/audio/metadata/session-download/`

## Authentication

None (public endpoints).

---

## Step 1: Create session (upload)

### POST /v1/audio/metadata/session/

**Description**  
Upload an audio file (or send a URL to an audio file). The server stores the file temporarily, returns the same metadata as `POST /v1/audio/metadata/full/` (see [audio_metadata.md](audio_metadata.md)), plus a **session token** and **session_expires_in_seconds** (900 = 15 minutes). Use the token in the download endpoint.

**Request**

Same as [audio_metadata.md](audio_metadata.md) full metadata:

- **Multipart**: `file` (required), `include_musicbrainz_analysis` (optional, boolean).
- **JSON**: `file` (URL string), `include_musicbrainz_analysis` (optional).

**Response**

Status: `200 OK`

Body: JSON with the same keys as full metadata (e.g. `title`, `artists_names`, `album_name`, …) plus:

- **session_token** (string): Opaque token. Send it in the download request (header `X-Session-Token` or body `session_token`).
- **session_expires_in_seconds** (number): 900 (15 minutes). Session is valid for this duration; you can call download multiple times until then.

Example (camelCase in actual response if using camelCase renderer):

```json
{
  "title": "My Track",
  "artists_names": ["Artist A"],
  "album_name": "My Album",
  "session_token": "a1b2c3d4e5f6...",
  "session_expires_in_seconds": 900
}
```

**Errors**  
Same as full metadata (400, 413 for invalid or oversized file).

---

## Step 2: Download (apply metadata and get file)

### POST /v1/audio/metadata/session-download/

**Description**  
Returns the file associated with the session token, with optional metadata written in. You can call this **multiple times** with the same token and different metadata; the session stays valid until it expires (15 minutes after creation).

**Request**

- **Session token**: Required. Send either:
  - Header: `X-Session-Token: <session_token>`
  - Or body: `session_token` (string) in JSON.
- **Metadata (optional)**: JSON body with any of: `title`, `artists_names`, `album_name`, `album_artists_names`, `genres_names` (list of strings), `rating`, `language`. Only provided fields are written; others are left as in the file. To get the file unchanged, send an empty body `{}` (but still provide the token in the header).

Body example:

```json
{
  "title": "New Title",
  "artists_names": ["Artist One", "Artist Two"],
  "album_name": "New Album",
  "genres_names": ["Rock", "Alternative"]
}
```

**Response**

- **200 OK**: Body is the audio file (binary). Headers include `Content-Disposition: attachment; filename="<original_filename>"`.
- **400 Bad Request**: Missing session token.
- **410 Gone**: Session not found or expired. Client should create a new session (upload again).

**Notes**

- The stored file is never modified; the server copies it, writes the requested metadata into the copy, and streams that copy. So the same session can be used for several downloads with different metadata.
- Session and temp file are removed automatically after 15 minutes (TTL). A periodic cleanup of the session directory is recommended for orphaned files.

**Storage**  
Session files are stored in the env-defined directory `METADATA_SESSION_DIR`. This directory is separate from `TMP_UPLOADED_FILES` (Django’s request upload temp dir): each has its own path. When `TMP_UPLOADED_FILES` is set, `METADATA_SESSION_DIR` must be set (via `METADATA_SESSION_DIR_INTERNAL` or `METADATA_SESSION_DIR_EXTERNAL` in the paths script). No default; the app fails to start if `METADATA_SESSION_DIR` is missing when uploads are enabled. On production deploy, `METADATA_SESSION_DIR_EXTERNAL` is supplied at runtime by the server or Compose environment (not by the deploy workflow).

---

## Summary

| Step | Endpoint | Action |
|------|----------|--------|
| 1 | `POST /v1/audio/metadata/session/` | Upload file (or URL); get metadata + `session_token` + `session_expires_in_seconds` (900). |
| 2 | `POST /v1/audio/metadata/session-download/` | Send `X-Session-Token` (or `session_token` in body) + optional metadata; get file with tags written. Repeatable until session expires. |

Session TTL: **15 minutes**. Multi-use: **yes** (multiple downloads per session).
