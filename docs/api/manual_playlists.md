# Manual Playlists

## Overview
Manage manual playlists

## Contexts
| Context | Base Path | Authentication | Description |
|--------|----------|----------------|-------------|
| `me` | `/v1/me/manual-playlists/` | Required | Manual playlists owned by the authenticated user |
| `reference` | `/v1/reference/manual-playlists/` | Optional / Public | System-owned reference resources (managed by account defined by TMTA_USERNAME environment variable) |

## Endpoints

#### List
`GET {base}`

#### Retrieve
`GET {base}{id}/`

#### Create
`POST {base}`

#### Update
`PUT {base}{id}/`

### Context Differences

#### Reference
- Read-only
- Public access
- Owned by system account (defined by TMTA_USERNAME environment variable)

#### Me
- Editable (create, update)
- Scoped to authenticated user