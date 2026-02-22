# Artists

## Overview
Manage artists

## Contexts
| Context | Base Path | Authentication | Description |
|--------|----------|----------------|-------------|
| `me` | `/v1/me/artists/` | Required | Artists associated with the authenticated user |
| `reference` | `/v1/reference/artists/` | Optional / Public | System-owned reference resources (managed by account defined by TMTA_USERNAME environment variable) |

## Endpoints

#### List
`GET {base}`

#### Retrieve
`GET {base}{id}/`

#### Delete
`DELETE {base}{id}/`

### Context Differences

#### Reference
- Managed internally by system account (defined by TMTA_USERNAME environment variable)

#### Me
- Scoped to authenticated user