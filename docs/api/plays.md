# Plays

## Overview

Manage play history

## Contexts

| Context     | Base Path              | Authentication    | Description                                                                                         |
| ----------- | ---------------------- | ----------------- | --------------------------------------------------------------------------------------------------- |
| `me`        | `/v1/me/plays/`        | Required          | Play history for the authenticated user                                                             |
| `reference` | `/v1/reference/plays/` | Optional / Public | System-owned reference play data (managed by account defined by TMTA_USERNAME environment variable) |

## Endpoints

#### List

`GET {base}`

#### Retrieve

`GET {base}{id}/`

#### Create

`POST {base}`

### Context Differences

#### Reference

- Managed internally by system account (defined by TMTA_USERNAME environment variable)

#### Me

- Scoped to authenticated user
- Allows creating new play records
