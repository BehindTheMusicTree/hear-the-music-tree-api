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
- Full CRUD operations
- Scoped to authenticated user