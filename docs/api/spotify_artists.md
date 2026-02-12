# spotify-artists

## Overview
Manage Spotify artists

## Base URL
/api/{APP_VERSION}/spotify-artists/

## Authentication
JWT token required

## Permissions
Authenticated users only (IsAuthenticated)

## Endpoints
| Method | Path | Action | Description |
|------|------|--------|-------------|
| GET | / | list | List Spotify artists |
| GET | /{id}/ | retrieve | Get Spotify artist details |

## Request / Response

### GET /

**Description**
List Spotify artists

**Request**
Headers:
Authorization: Bearer {token}

Query params:
page, page_size, name, popularity_min, popularity_max, created_on, updated_on

Body:
```json
{}
```

**Response**
Status codes:
 | 00 OK

Body:
```json
{
  "count": 10,
  "next": null,
  "previous": null,
  "results": [
    {
      "spotify_id": "string",
      "name": "string",
      "popularity": 50,
      "spotify_link": "string",
      "genres": ["string"],
      "images": []
    }
  ]
}
```

### Validation Rules
None

### Business Rules
None

### Errors
| Code | Meaning |
|------|----------|
| 400 | Bad Request - Invalid parameters |
| 401 | Unauthorized - Invalid token |
| 404 | Not Found - Artist not found |

### Versioning
TODO

### Notes
TODO

### GET /{id}/

**Description**
Get Spotify artist details

**Request**
Headers:
Authorization: Bearer {token}

Query params:
None

Body:
```json
{}
```

**Response**
Status codes:
 | 00 OK

Body:
```json
{
  "spotify_id": "string",
  "name": "string",
  "popularity": 50,
  "spotify_link": "string",
  "genres": ["string"],
  "images": []
}
```

### Validation Rules
None

### Business Rules
None

### Errors
| Code | Meaning |
|------|----------|
| 400 | Bad Request - Invalid parameters |
| 401 | Unauthorized - Invalid token |
| 404 | Not Found - Artist not found |

### Versioning
{APP_VERSION}

### Notes
None