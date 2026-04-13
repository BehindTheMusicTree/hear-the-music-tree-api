# Genre Playlists

## Overview

Manage playlists based on genres.

## Contexts

| Context     | Base Path                        | Authentication    | Description                                                                                         |
| ----------- | -------------------------------- | ----------------- | --------------------------------------------------------------------------------------------------- |
| `me`        | `/v1/me/genre-playlists/`        | Required          | Genre playlists owned by the authenticated user                                                     |
| `reference` | `/v1/reference/genre-playlists/` | Optional / Public | System-owned reference resources (managed by account defined by TMTA_USERNAME environment variable) |

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
