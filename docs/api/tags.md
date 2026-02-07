# Tags

## Overview
Manage tag hierarchies and trees.

## Contexts
| Context | Base Path | Authentication | Description |
|--------|----------|----------------|-------------|
| `me` | `/api/{version}/me/tags/` | Required | Tags owned by the authenticated user |
| `reference` | `/api/{version}/reference/tags/` | Optional / Public | System-owned reference resources (managed by account defined by TMTA_USERNAME environment variable) |

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

#### Tree
`GET {base}tree/`

#### Import Tree
`POST {base}tree/import/`

### Context Differences

#### Reference
- Managed internally by system account (defined by TMTA_USERNAME environment variable)
- Includes tree operations for loading reference data

#### Me
- Fully editable
- Scoped to authenticated user