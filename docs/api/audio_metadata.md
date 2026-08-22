# Audio metadata (read raw)

## Overview

Extract raw metadata from an audio file without storing it. The file is read only; no resource is created and the file is not persisted.

## Base URL

/v1/audio/metadata/full/

## Authentication

None (public endpoint)

## Endpoints

| Method | Path | Action  | Description                                                  |
| ------ | ---- | ------- | ------------------------------------------------------------ |
| POST   | /    | extract | Send an audio file and receive its embedded metadata as JSON |

## Request / Response

### POST /

**Description**
Upload an audio file and get back all readable metadata (tags and technical properties) from the file. The file is not saved; the response is computed from the uploaded bytes.

**Request**

Headers:

- `Content-Type`: `multipart/form-data` (required)

Body (multipart form):

- `file` (required): One audio file. Supported formats: `.mp3`, `.flac`, `.wav`. Max size is defined by server configuration (see `UPLOADED_TRACK_FILE_SIZE_MAX_IN_MO`).
- `include_musicbrainz_analysis` (optional): Boolean. When `true`, the response includes a `musicbrainz_raw_data` key with raw AcoustID/MusicBrainz lookup result (or an error payload if fingerprinting or lookup fails). Default: `false`. No authentication required.

**Response**

Status: `200 OK`

Body: JSON object with raw metadata and optional technical fields. Keys may be omitted when not present in the file.

```json
{
  "title": "string | null",
  "artists_names": ["string"],
  "album_name": "string | null",
  "album_artists_names": ["string"],
  "genres_names": ["string"],
  "rating": "number | null",
  "language": "string | null",
  "duration_sec": "number",
  "bitrate_kbps": "number",
  "size_bytes": "number"
}
```

- **title**: Track title
- **artists_names**: List of artist names
- **album_name**: Album name
- **album_artists_names**: List of album artist names
- **genres_names**: List of genre names
- **rating**: Rating (format-dependent; may be normalized)
- **language**: Language code
- **duration_sec**: Duration in seconds (technical)
- **bitrate_kbps**: Bitrate in kbps (technical)
- **size_bytes**: File size in bytes (technical)

### Validation rules

- `file` is required.
- File extension must be one of: `.mp3`, `.flac`, `.wav`.
- File size must not exceed the server limit.
- File content must be valid audio (magic bytes / format validated).

### Errors

| Code | Meaning                                                                                  |
| ---- | ---------------------------------------------------------------------------------------- |
| 400  | Bad Request — missing file, invalid format, file too large, or corrupted / invalid audio |
| 413  | Payload Too Large — file exceeds maximum size                                            |

### Versioning

API path prefix uses the major version only (e.g. `v1`), derived from `APP_VERSION`.

### Notes

- Metadata is merged from all formats present in the file (e.g. ID3v1 + ID3v2 for MP3). Format-specific behaviour is documented in `hear/utils/audio_file_metadata/README.md`.
- Not all fields are supported by every format (e.g. album artist is not supported by ID3v1).

### When `include_musicbrainz_analysis` is true

The response includes an additional key **`musicbrainz_raw_data`**:

- **Success**: Object is the raw best-recording dict from AcoustID (e.g. `id`, `title`, `duration`, `artists`, `releasegroups`, `score`).
- **Fingerprint failure**: Object is `{ "error": "fingerprint_failed", "code": "<code>", "message": "<message>" }`.
- **MusicBrainz lookup failure or no match**: Object is `{ "error": "<code>", "code": "<code>", "message": "<message>" }` (e.g. `no_match`, `duration_below_or_equal_1_sec`).
