# Manual Playlists

## Overview
Manage manual playlists

## Contexts
| Context | Base Path | Authentication | Description |
|--------|----------|----------------|-------------|
| `me` | `/api/{version}/me/manual-playlists/` | Required | Manual playlists owned by the authenticated user |
| `reference` | `/api/{version}/reference/manual-playlists/` | Optional / Public | System-owned reference resources (managed by account defined by TMTA_USERNAME environment variable) |

## Endpoints

#### List
`GET {base}`

#### Retrieve
`GET {base}{id}/`

#### Create
`POST {base}`

#### Update
`PUT {base}{id}/`

#### Delete
`DELETE {base}{id}/`

### Context Differences

#### Reference
- Read-only
- Public access
- Owned by system account (defined by TMTA_USERNAME environment variable)

#### Me
- Editable by owner
- Scoped to authenticated user