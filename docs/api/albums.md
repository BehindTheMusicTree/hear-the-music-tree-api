# albums

## Overview
Manage albums

## Base URL
/api/{APP_VERSION}/albums/

## Authentication
JWT token required

## Permissions
Authenticated users only (IsAuthenticated)

## Endpoints
| Method | Path | Action | Description |
|------|------|--------|-------------|
| GET | / | list | List albums |
| GET | /{id}/ | retrieve | Get album details |
| DELETE | /{id}/ | destroy | Delete album |

## Request / Response

### GET /

**Description**
List albums

**Request**
Headers:
Authorization: Bearer {token}

Query params:
page, page_size, name, album_artist_name

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
      "uuid": "uuid",
      "name": "string",
      "year": 2023,
      "album_artists": [],
      "uploaded_tracks_sorted": [],
      "uploaded_tracks_count": 10,
      "uploaded_tracks_archived_count": 0,
      "duration_in_sec": 3600,
      "duration_str_in_hour_min_sec": "1:00:00",
      "created_on": "2023-01-01T00:00:00Z",
      "updated_on": "2023-01-01T00:00:00Z"
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
 | 00	Bad Request - Invalid parameters
 | 01	Unauthorized - Invalid token
 | 04	Not Found - Album not found

### Versioning
TODO

### Notes
TODO	

### GET /{id}/

**Description**
Get album details

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
  "uuid": "uuid",
  "name": "string",
  "year": 2023,
  "album_artists": [],
  "uploaded_tracks_sorted": [],
  "uploaded_tracks_count": 10,
  "uploaded_tracks_archived_count": 0,
  "duration_in_sec": 3600,
  "duration_str_in_hour_min_sec": "1:00:00",
  "created_on": "2023-01-01T00:00:00Z",
  "updated_on": "2023-01-01T00:00:00Z"
}
```

### Validation Rules
None

### Business Rules
None

### Errors
| Code | Meaning |
|------|----------|
 | 00	Bad Request - Invalid parameters
 | 01	Unauthorized - Invalid token
 | 04	Not Found - Album not found

### Versioning
TODO

### Notes
TODO	

### DELETE /{id}/

**Description**
Delete album

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
 | 04 No Content

Body:
```json
{}
```

### Validation Rules
None

### Business Rules
None

### Errors
| Code | Meaning |
|------|----------|
 | 00	Bad Request - Invalid parameters
 | 01	Unauthorized - Invalid token
 | 04	Not Found - Album not found

### Versioning
TODO

### Notes
TODO
 | 01	Unauthorized - Invalid token
 | 04	Not Found - Album not found	

### Versioning

{APP_VERSION}

### Notes
None