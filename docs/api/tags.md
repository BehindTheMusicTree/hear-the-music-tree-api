# Tags

## Overview

Manage tag hierarchies and trees.

## Contexts

| Context | Base Path      | Authentication | Description                          |
| ------- | -------------- | -------------- | ------------------------------------ |
| `me`    | `/v1/me/tags/` | Required       | Tags owned by the authenticated user |

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
