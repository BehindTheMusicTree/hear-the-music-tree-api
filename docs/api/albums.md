# Albums

## Overview
Manage album information.

## Contexts
| Context | Base Path | Authentication | Description |
|--------|----------|----------------|-------------|
| `me` | `/v1/me/albums/` | Required | Albums in authenticated user's library |
| `reference` | `/v1/reference/albums/` | Optional / Public | System-owned reference resources (managed by account defined by TMTA_USERNAME environment variable) |

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