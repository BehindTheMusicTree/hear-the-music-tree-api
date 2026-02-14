# Library Spotify

## Overview
Manage Spotify library tracks in user library.

## Contexts
| Context | Base Path | Authentication | Description |
|--------|----------|----------------|-------------|
| `me` | `/api/{version}/me/library/spotify/` | Required | Spotify tracks in the authenticated user's library |
| `reference` | `/api/{version}/reference/library/spotify/` | Optional / Public | System-owned reference Spotify resources |

## Endpoints

#### List
`GET {base}`

#### Retrieve
`GET {base}{id}/`

#### Quick Sync
`POST {base}sync/quick/`

Performs a quick sync of the user's Spotify library. This only fetches new additions since the last sync and is faster than a full sync.

#### Full Sync
`POST {base}sync/full/`

Performs a full sync of the user's Spotify library. This checks for both additions and removals, but is more resource-intensive.

### Context Differences

#### Reference
- Read-only
- Public access
- Owned by system account

#### Me
- Read-only for tracks
- Sync operations available
- Scoped to authenticated user