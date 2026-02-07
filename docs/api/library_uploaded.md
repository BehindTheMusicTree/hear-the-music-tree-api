# library/uploaded

## Overview
Manage uploaded tracks

## Base URL
/api/{APP_VERSION}/library/uploaded/

## Authentication
JWT token required

## Permissions
Authenticated users only (IsAuthenticated)

## Endpoints
| Method | Path | Action | Description |
|------|------|--------|-------------|
| GET | / | list | List uploaded tracks |
| POST | / | create | Upload a new track |
| GET | /{id}/ | retrieve | Get track details |
| PUT | /{id}/ | update | Update track |
| DELETE | /{id}/ | destroy | Delete track |
| GET | /{id}/download/ | download | Download track file |

## Request / Response

### GET /

**Description**
List uploaded tracks

**Request**
Headers:
Authorization: Bearer {token}

Query params:
page, page_size, title, artists_name, album_name, genre_name, language

Body:
None

**Response**
Status codes:
200 OK

Body:
```json
{
  "count": 10,
  "next": null,
  "previous": null,
  "results": [
    {
      "uuid": "uuid",
      "relative_url": "string",
      "title": "string",
      "file": {},
      "artists": [],
      "album": {},
      "track_number": 1,
      "genre": {},
      "rating": 5,
      "language": "string",
      "playlists": [],
      "play_count": 0,
      "archived": false,
      "created_on": "2023-01-01T00:00:00Z",
      "updated_on": "2023-01-01T00:00:00Z"
    }
  ]
}
```

Validation Rules
None

Business Rules
None

Errors
Code	Meaning
400	Bad Request - Invalid parameters
401	Unauthorized - Invalid token
404	Not Found - Track not found	

### POST /

**Description**
Upload a new track

**Request**
Headers:
Authorization: Bearer {token}
Content-Type: multipart/form-data

Query params:
None

Body:
```json
{
  "file": "file",
  "title": "string",
  "artists_names": ["string"],
  "album_name": "string",
  "album_artists_names": ["string"],
  "track_number": 1,
  "genre": "string",
  "rating": 5,
  "language": "string",
  "track_file_fingerprint_must_be_unique": true
}
```

**Response**
Status codes:
201 Created

Body:
```json
{
  "uuid": "uuid",
  "relative_url": "string",
  "title": "string",
  "file": {},
  "artists": [],
  "album": {},
  "track_number": 1,
  "genre": {},
  "rating": 5,
  "language": "string",
  "playlists": [],
  "play_count": 0,
  "archived": false,
  "created_on": "2023-01-01T00:00:00Z",
  "updated_on": "2023-01-01T00:00:00Z"
}
```

Validation Rules
File required, title max length, etc.

Business Rules
File metadata extraction, title generation if not provided

Errors
Code	Meaning
400	Bad Request - Invalid file or parameters
401	Unauthorized - Invalid token	

### GET /{id}/

**Description**
Get track details

**Request**
Headers:
Authorization: Bearer {token}

Query params:
None

Body:
None

**Response**
Status codes:
200 OK

Body:
```json
{
  "uuid": "uuid",
  "relative_url": "string",
  "title": "string",
  "file": {},
  "artists": [],
  "album": {},
  "track_number": 1,
  "genre": {},
  "rating": 5,
  "language": "string",
  "playlists": [],
  "play_count": 0,
  "archived": false,
  "created_on": "2023-01-01T00:00:00Z",
  "updated_on": "2023-01-01T00:00:00Z"
}
```

Validation Rules
None

Business Rules
None

Errors
Code	Meaning
400	Bad Request - Invalid parameters
401	Unauthorized - Invalid token
404	Not Found - Track not found	

### PUT /{id}/

**Description**
Update track

**Request**
Headers:
Authorization: Bearer {token}

Query params:
None

Body:
```json
{
  "title": "string",
  "artists_names": ["string"],
  "album_name": "string",
  "album_artists_names": ["string"],
  "track_number": 1,
  "genre": "string",
  "rating": 5,
  "language": "string"
}
```

**Response**
Status codes:
200 OK

Body:
```json
{
  "uuid": "uuid",
  "relative_url": "string",
  "title": "string",
  "file": {},
  "artists": [],
  "album": {},
  "track_number": 1,
  "genre": {},
  "rating": 5,
  "language": "string",
  "playlists": [],
  "play_count": 0,
  "archived": false,
  "created_on": "2023-01-01T00:00:00Z",
  "updated_on": "2023-01-01T00:00:00Z"
}
```

Validation Rules
Title max length, etc.

Business Rules
Album/artist creation if not exist

Errors
Code	Meaning
400	Bad Request - Invalid parameters
401	Unauthorized - Invalid token
404	Not Found - Track not found	

### DELETE /{id}/

**Description**
Delete track

**Request**
Headers:
Authorization: Bearer {token}

Query params:
None

Body:
None

**Response**
Status codes:
204 No Content

Body:
None

Validation Rules
None

Business Rules
None

Errors
Code	Meaning
400	Bad Request - Invalid parameters
401	Unauthorized - Invalid token
404	Not Found - Track not found	

### GET /{id}/download/

**Description**
Download track file

**Request**
Headers:
Authorization: Bearer {token}

Query params:
None

Body:
None

**Response**
Status codes:
200 OK

Body:
File binary

Validation Rules
None

Business Rules
None

Errors
Code	Meaning
401	Unauthorized - Invalid token
404	Not Found - Track or file not found	

Versioning

{APP_VERSION}

Notes
None