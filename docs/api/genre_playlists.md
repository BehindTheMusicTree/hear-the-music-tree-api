# Genre Playlists

## Overview
Manage playlists based on genres.

## Contexts
| Context | Base Path | Authentication | Description |
|--------|----------|----------------|-------------|
| `me` | `/api/{version}/me/genre-playlists/` | Required | Genre playlists owned by the authenticated user |
| `reference` | `/api/{version}/reference/genre-playlists/` | Optional / Public | System-owned reference resources (managed by account defined by TMTA_USERNAME environment variable) |

## Endpoints

#### List
`GET {base}`

#### Retrieve
`GET {base}{id}/`

### Context Differences

#### Reference
- Read-only
- Public access
- Owned by system account (defined by TMTA_USERNAME environment variable)

#### Me
- Editable by owner
- Scoped to authenticated user