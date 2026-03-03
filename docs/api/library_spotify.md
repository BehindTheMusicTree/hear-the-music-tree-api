# Library Spotify

## Overview
Manage Spotify library tracks in the authenticated user's library. Each user must link their own Spotify account; there is no shared or system-owned Spotify library (see [Spotify compliance](../integrations/spotify.md#no-shared-system-spotify-account)).

## Context
| Context | Base Path | Authentication | Description |
|--------|----------|----------------|-------------|
| `me` | `/v1/me/library/spotify/` | Required | Spotify tracks in the authenticated user's library |

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

### Me context
- Read-only for tracks
- Sync operations available
- Scoped to authenticated user