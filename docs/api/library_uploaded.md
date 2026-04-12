# Library Uploaded

## Overview
Manage uploaded tracks in user library.

## Contexts
| Context | Base Path | Authentication | Description |
|--------|----------|----------------|-------------|
| `me` | `/v1/me/library/uploaded/` | Required | Uploaded tracks owned by the authenticated user |
| `reference` | `/v1/reference/library/uploaded/` | Optional / Public | System-owned reference resources (managed by account defined by TMTA_USERNAME environment variable) |

## Endpoints

#### List
`GET {base}`

#### Retrieve
`GET {base}{id}/`

#### Create
`POST {base}`

**Request**
- **File or URL**: Send the track as a multipart file upload or as a URL string (same field). Supported formats: `.mp3`, `.flac`, `.wav`. URL must be reachable (HTTP 200 or 206).
- **Title** (optional): If omitted, the title is derived from the file name (extension stripped, after removing configured substrings). If the file name exceeds the server filename length limit, a generated title with the configured prefix is used instead.

#### Update
`PUT {base}{id}/`

**Validation (400 Bad Request)**
- `album_artists_names` provided without `album_name` (album name is required when album artists field is provided).
- `track_number` provided with a value without `album_name` (album name must be specified if track position is).

#### Delete
`DELETE {base}{id}/`

### Context Differences

#### Reference
- Read-only
- Public access
- Owned by system account (defined by TMTA_USERNAME environment variable)

#### Me
- Full CRUD operations
- Scoped to authenticated user