# HearTheMusicTree API

[![License](https://img.shields.io/badge/license-Apache%202.0-blue.svg)](LICENSE)
[![Python](https://img.shields.io/badge/python-3.14-blue.svg)](https://www.python.org/)
[![Django](https://img.shields.io/badge/django-5.2-green.svg)](https://www.djangoproject.com/)

## Table of Contents

- [Introduction](#introduction)
  - [Mission](#mission)
  - [Key Features](#key-features)
  - [Ecosystem Integration](#ecosystem-integration)
- [Features](#features)
- [Vision](VISION.md)
- [Getting Started](#getting-started)
  - [Developer environment (recommended)](#developer-environment-recommended)
- [API](#api)
  - [Base URL & Interactive Documentation](#base-url--interactive-documentation)
  - [Authentication](#authentication)
    - [Obtaining Tokens](#obtaining-tokens)
    - [Refreshing Tokens](#refreshing-tokens)
    - [Using Tokens](#using-tokens)
    - [Spotify Authentication](#spotify-authentication)
  - [Endpoints Reference](#endpoints-reference)
    - [Authentication](#authentication-1)
    - [Library Management](#library-management)
    - [Music Metadata](#music-metadata)
    - [Genres (me)](#genres-me)
    - [Reference Genres](#reference-genres)
    - [Tags (me)](#tags-me)
    - [Reference Tags](#reference-tags)
    - [Playlists](#playlists)
    - [Play History](#play-history)
    - [Search](#search)
    - [User Management](#user-management)
- [Usage](#usage)
  - [Basic Workflow](#basic-workflow)
  - [Advanced Features](#advanced-features)
  - [Error Handling](#error-handling)
- [Technical Details](#technical-details)
  - [Audio Metadata Handling](#audio-metadata-handling)
  - [MusicBrainz Integration](#musicbrainz-integration)
  - [Shared Reference Data (TMTA System User)](#shared-reference-data-tmta-system-user)
- [Contributing](#contributing)
- [License](#license)
- [Acknowledgements](#acknowledgements)

## Introduction

HearTheMusicTree API is a cloud-based audio file manager that empowers music collectors, DJs, curators, and listeners to organize and discover music through powerful metadata handling, genre intelligence, and cross-platform synchronization. This project is part of the [BehindTheMusicTree ecosystem](https://github.com/behindthemusictree) — a collection of open-source tools designed to transform music libraries into living, contextualized experiences.

### Mission

HearTheMusicTree aims to provide a user-first, extensible platform for organizing and discovering music that respects cultural diversity and provides meaningful musical context. We focus on personal library management, privacy, and local ownership while remaining open-source and interoperable.

### Key Features

- **Metadata-First Approach**: Treat metadata as first-class data — accurate, normalized, and machine-readable
- **Genre Intelligence**: Leverage community-driven taxonomy from GrowTheMusicTree for improved categorization and discovery
- **Smart Playlists**: Automatically generate playlists from genre hierarchies and user preferences
- **Universal Format Support**: Handle common audio containers and tags with consistent metadata operations
- **API-First Design**: RESTful API for all core functionality, enabling integrations with clients, DJ tools, and research applications
- **Privacy & Security**: Secure storage with respect for user privacy and data ownership

### Ecosystem Integration

HearTheMusicTree integrates seamlessly with other projects in the BehindTheMusicTree ecosystem:

- **[AudioMeta Python](https://github.com/BehindTheMusicTree/audiometa)**: Reliable metadata reading and updating across formats (ID3v1, ID3v2, Vorbis, RIFF)
- **[GrowTheMusicTree](https://github.com/BehindTheMusicTree/grow-the-music-tree)**: Community-driven taxonomy curation for classification and playlist generation
- **[TheMusicTreeAPI](https://github.com/BehindTheMusicTree/the-music-tree-api)**: Authoritative RESTful endpoints for genre references, hierarchies, and detection

> **⚠️ Note**: The API is currently undergoing server migration and is not available online. Please set up a local development environment to use the API. See [Getting Started](#getting-started) for setup instructions.

For more details about our vision, goals, and roadmap, see [VISION.md](VISION.md).

## Features

- **Upload Tracks**: Easily upload your music tracks to the platform.
- **Tag Tracks**: Tag your tracks with metadata such as artist names, album titles, and more. This tagging process helps organize your music files.
- **Rate Tracks**: Users can rate tracks, providing a way to highlight popular or preferred songs.
- **Create Genre Hierarchies**: The most important feature of HearTheMusicTree API is the ability to create a hierarchy of music genres. For example, if a track is tagged as "techno," it will automatically be included in both the "techno" playlist and the broader "electronic music" playlist.

## Getting Started

For detailed setup and installation instructions, please see the [Contributing Guidelines](CONTRIBUTING.md#1-environment-setup).

**Quick Start:**

<!-- Use an HTML table so we can set column widths on GitHub render -->
<table>
  <colgroup>
    <col style="width: 25%;" />
    <col style="width: 75%;" />
  </colgroup>
  <thead>
    <tr>
      <th style="text-align: left;">Requirement</th>
      <th style="text-align: left;">Details</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td><strong>Python</strong></td>
      <td>3.14</td>
    </tr>
    <tr>
      <td><strong>Containerization</strong></td>
      <td>Docker &amp; Docker Compose</td>
    </tr>
    <tr>
      <td><strong>Database</strong></td>
      <td>PostgreSQL</td>
    </tr>
    <tr>
      <td><strong>Setup Guide</strong></td>
      <td>See <a href="CONTRIBUTING.md">CONTRIBUTING.md</a> for full setup instructions</td>
    </tr>
  </tbody>
</table>

### Developer environment (recommended)

To keep a consistent, reproducible development environment across contributors, we recommend creating a workspace-local virtual environment named `.venv` in the project root and pointing Visual Studio Code to use that interpreter.

1) Create a `.venv` in the project root:

```bash
python3 -m venv .venv
```

2) Activate the virtualenv:

- macOS / Linux:
	```bash
	source .venv/bin/activate
	```
- Windows (PowerShell):
	```powershell
	.\.venv\Scripts\Activate.ps1
	```

3) Install dependencies:
```bash
pip install -r requirements.txt
```

4) VS Code setup
- The repository workspace settings now reference `${workspaceFolder}/.venv/bin/python` (instead of a machine-local absolute path) so VS Code will automatically pick the correct interpreter if your `.venv` is in the project root.
- Alternatively, run the VS Code command `Python: Select Interpreter` and choose `.venv/bin/python`.

If you prefer a different venv name or layout, adjust your local VS Code interpreter selection. The repository stores a workspace-relative default to keep experience consistent for new contributors.

## API

### Base URL & Interactive Documentation

#### Base URL

The API base URL follows the pattern: `{version}/`

For example: `v1/`

The API version is configured via the `APP_VERSION` environment variable.

> **Note**: Since the API is currently undergoing server migration and is not available online, all examples in this documentation use `http://localhost:8000` as the base URL. When running locally, replace this with your local server address if different.

#### Interactive Documentation

The API provides interactive documentation using OpenAPI (OAS 3.x):

- **Swagger UI**: `http://localhost:8000/docs/` — Interactive API explorer with try-it-out functionality
- **ReDoc**: `http://localhost:8000/schema/redoc/` — Alternative API documentation with a readable layout
- **OpenAPI Schema**: `http://localhost:8000/schema/` — Raw OpenAPI schema (JSON or YAML via content negotiation) for code generation and tooling

**How the schema is generated**: The schema is produced at runtime by [drf-spectacular](https://drf-spectacular.readthedocs.io/), which introspects Django REST Framework views and serializers. The OpenAPI **title** (shown in Swagger/ReDoc) is set via the `OPENAPI_TITLE` env var, defaulting to `APP_NAME`; the **version** (in `info.version`) is taken from `APP_VERSION` so it matches the API app version. The project uses a custom schema class (`api.view.schema.AppAutoSchema`) so that Django `GeneratedField` and `DecimalField` (e.g. on `TrackFile`) are mapped correctly; otherwise schema generation would raise when visiting `/schema/` or `/docs/`. The schema always reflects the current API; no separate hand-written spec is required for the served docs.

> **Quick Access**: When running the development server locally, visit [http://localhost:8000/api/docs/](http://localhost:8000/api/docs/) to explore the API interactively.

### Authentication

The API uses JWT (JSON Web Tokens) for authentication. Most endpoints require authentication.

#### Obtaining Tokens

**Endpoint**: `POST /api/{version}/auth/token/`

**Request Body**:
```json
{
  "username": "your_username",
  "password": "your_password"
}
```

**Response**:
```json
{
  "access": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "refresh": "eyJ0eXAiOiJKV1QiLCJhbGc..."
}
```

#### Refreshing Tokens

**Endpoint**: `POST /api/{version}/auth/token/refresh/`

**Request Body**:
```json
{
  "refresh": "your_refresh_token"
}
```

**Response**:
```json
{
  "access": "eyJ0eXAiOiJKV1QiLCJhbGc..."
}
```

#### Using Tokens

Include the access token in the `Authorization` header:

```
Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGc...
```

**Token Lifetime**:
- Access tokens: 100 minutes
- Refresh tokens: 1 day

#### Spotify Authentication

The API supports authentication via Spotify OAuth, allowing users to sign in with their Spotify account.

**OAuth Flow**:

1. **Redirect to Spotify Authorization**: Your frontend should redirect users to Spotify's authorization URL to obtain an authorization code. The authorization URL should include:
   - `client_id`: Your Spotify app client ID
   - `redirect_uri`: Your registered redirect URI
   - `scope`: Required scopes (e.g., `user-read-email user-read-private user-library-read`)
   - `response_type`: `code`
   - `state`: Optional state parameter for CSRF protection

2. **Exchange Code for Tokens**: After the user authorizes, Spotify redirects back with an authorization `code`. Send this code to the API:

**Endpoint**: `POST /api/{version}/auth/spotify/`

**Request Body**:
```json
{
  "code": "spotify_authorization_code"
}
```

**Response**:
```json
{
  "accessToken": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "refreshToken": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "expires_at": "2024-01-15T12:00:00Z",
  "spotifyUser": {
    "spotify_profile": {
      "id": "spotify_user_id",
      "display_name": "User Name",
      "email": "user@example.com",
      "followers": {...},
      "images": [...],
      "uri": "spotify:user:..."
    },
    "id": 123,
    "email": "user@example.com",
    "spotify_id": "spotify_user_id",
    "display_name": "User Name",
    "followers": {...},
    "href": "https://api.spotify.com/v1/users/...",
    "images": [...],
    "type": "user",
    "uri": "spotify:user:..."
  }
}
```

**What Happens**:
- The API exchanges the authorization code for Spotify access and refresh tokens
- Creates or updates a Spotify user account in the system
- Returns JWT tokens (access and refresh) for API authentication
- Returns Spotify user profile information

**Using the JWT Token**:
After Spotify authentication, use the returned `accessToken` as a JWT Bearer token for subsequent API requests, just like with regular JWT authentication:

```
Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGc...
```

**Note**: For detailed setup instructions and Spotify API configuration, see the [Spotify Integration documentation](api/utils/spotify_api/README.md).

### Endpoints Reference

Legend: 🔒 = Requires authentication | 🔓 = No authentication required

All endpoints are prefixed with the API base URL (`{version}/`). Most endpoints require authentication via JWT Bearer token.

### Authentication

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| `POST` | `auth/token/` | Obtain JWT access and refresh tokens | 🔓 |
| `POST` | `auth/token/refresh/` | Refresh access token | 🔓 |
| `POST` | `auth/spotify/` | Authenticate with Spotify | 🔓 |

### Library Management

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| `GET` | `library/uploaded/` | List uploaded tracks | 🔒 |
| `POST` | `library/uploaded/` | Upload a new track | 🔒 |
| `GET` | `library/uploaded/{id}/` | Retrieve a specific uploaded track | 🔒 |
| `PUT` | `library/uploaded/{id}/` | Update an uploaded track | 🔒 |
| `DELETE` | `library/uploaded/{id}/` | Delete an uploaded track | 🔒 |
| `GET` | `library/spotify/` | List Spotify library tracks | 🔒 |
| `GET` | `library/spotify/{id}/` | Retrieve a specific Spotify track | 🔒 |
| `GET` | `all-tracks/` | Get all tracks (uploaded and Spotify) | 🔒 |

### Music Metadata

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| `GET` | `artists/` | List artists | 🔒 |
| `POST` | `artists/` | Create an artist | 🔒 |
| `GET` | `artists/{id}/` | Retrieve a specific artist | 🔒 |
| `PUT` | `artists/{id}/` | Update an artist | 🔒 |
| `DELETE` | `artists/{id}/` | Delete an artist | 🔒 |
| `GET` | `albums/` | List albums | 🔒 |
| `POST` | `albums/` | Create an album | 🔒 |
| `GET` | `albums/{id}/` | Retrieve a specific album | 🔒 |
| `PUT` | `albums/{id}/` | Update an album | 🔒 |
| `DELETE` | `albums/{id}/` | Delete an album | 🔒 |
| `GET` | `spotify-artists/` | List Spotify artists | 🔒 |
| `GET` | `spotify-artists/{id}/` | Retrieve a specific Spotify artist | 🔒 |

### Genres (me)

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| `GET` | `me/genres/` | List genres | 🔒 |
| `POST` | `me/genres/` | Create a genre | 🔒 |
| `GET` | `me/genres/{id}/` | Retrieve a specific genre | 🔒 |
| `PUT` | `me/genres/{id}/` | Update a genre | 🔒 |
| `DELETE` | `me/genres/{id}/` | Delete a genre | 🔒 |
| `GET` | `me/genres/tree/` | Get genres tree | 🔒 |
| `POST` | `me/genres/tree/import/` | Import genres tree | 🔒 |

### Reference Genres

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| `GET` | `reference/genres/` | List reference genres | 🔓 |
| `POST` | `reference/genres/` | Create a reference genre | 🔓 |
| `GET` | `reference/genres/{id}/` | Retrieve a reference genre | 🔓 |
| `PUT` | `reference/genres/{id}/` | Update a reference genre | 🔓 |
| `DELETE` | `reference/genres/{id}/` | Delete a reference genre | 🔓 |
| `GET` | `reference/genres/tree/` | Get reference genres tree | 🔓 |
| `POST` | `reference/genres/tree/import/` | Import reference genres tree | 🔓 |

### Tags (me)

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| `GET` | `me/tags/` | List tags | 🔒 |
| `POST` | `me/tags/` | Create a tag | 🔒 |
| `GET` | `me/tags/{id}/` | Retrieve a specific tag | 🔒 |
| `PUT` | `me/tags/{id}/` | Update a tag | 🔒 |
| `DELETE` | `me/tags/{id}/` | Delete a tag | 🔒 |
| `GET` | `me/tags/tree/` | Get tags tree | 🔒 |
| `POST` | `me/tags/tree/import/` | Import tags tree | 🔒 |

### Reference Tags

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| `GET` | `reference/tags/` | List reference tags | 🔓 |
| `POST` | `reference/tags/` | Create a reference tag | 🔓 |
| `GET` | `reference/tags/{id}/` | Retrieve a reference tag | 🔓 |
| `PUT` | `reference/tags/{id}/` | Update a reference tag | 🔓 |
| `DELETE` | `reference/tags/{id}/` | Delete a reference tag | 🔓 |
| `GET` | `reference/tags/tree/` | Get reference tags tree | 🔓 |
| `POST` | `reference/tags/tree/import/` | Import reference tags tree | 🔓 |

### Playlists

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| `GET` | `me/playlists/` | List my playlists | 🔒 |
| `GET` | `me/playlists/{id}/` | Retrieve a specific playlist | 🔒 |
| `GET` | `reference/playlists/` | List reference playlists | 🔓 |
| `GET` | `reference/playlists/{id}/` | Retrieve a reference playlist | 🔓 |
| `GET` | `me/manual-playlists/` | List my manual playlists | 🔒 |
| `POST` | `me/manual-playlists/` | Create a manual playlist | 🔒 |
| `GET` | `me/manual-playlists/{id}/` | Retrieve a manual playlist | 🔒 |
| `PUT` | `me/manual-playlists/{id}/` | Update a manual playlist | 🔒 |
| `GET` | `reference/manual-playlists/` | List reference manual playlists | 🔓 |
| `GET` | `reference/manual-playlists/{id}/` | Retrieve a reference manual playlist | 🔓 |
| `GET` | `me/genre-playlists/` | List my genre-based playlists | 🔒 |
| `GET` | `me/genre-playlists/{id}/` | Retrieve a genre playlist | 🔒 |
| `GET` | `reference/genre-playlists/` | List reference genre playlists | 🔓 |
| `GET` | `reference/genre-playlists/{id}/` | Retrieve a reference genre playlist | 🔓 |
| `GET` | `me/tag-playlists/` | List my tag-based playlists | 🔒 |
| `GET` | `me/tag-playlists/{id}/` | Retrieve a tag playlist | 🔒 |
| `GET` | `reference/tag-playlists/` | List reference tag playlists | 🔓 |
| `GET` | `reference/tag-playlists/{id}/` | Retrieve a reference tag playlist | 🔓 |

### Play History

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| `GET` | `plays/` | List play history | 🔒 |
| `POST` | `plays/` | Record a play | 🔒 |
| `GET` | `plays/{id}/` | Retrieve a specific play record | 🔒 |

### Search

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| `GET` | `search/` | Search across tracks, albums, artists, and playlists | 🔒 |

**Query Parameters**:
- `query`: Search query string
- `type`: Filter by type (track, album, artist, playlist)

### User Management

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| `GET` | `users/` | List users | 🔒 |
| `POST` | `users/` | Create a user | 🔒 |
| `GET` | `users/{id}/` | Retrieve a specific user | 🔒 |
| `PUT` | `users/{id}/` | Update a user | 🔒 |
| `DELETE` | `users/{id}/` | Delete a user | 🔒 |
| `GET` | `users/spotify/` | List Spotify users | 🔒 |
| `GET` | `users/spotify/{id}/` | Retrieve a specific Spotify user | 🔒 |

## Usage

### Basic Workflow

#### 1. Authenticate

```bash
curl -X POST http://localhost:8000/v1/auth/token/ \
  -H "Content-Type: application/json" \
  -d '{
    "username": "your_username",
    "password": "your_password"
  }'
```

Response:
```json
{
  "access": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "refresh": "eyJ0eXAiOiJKV1QiLCJhbGc..."
}
```

#### 2. Upload a Track

```bash
curl -X POST http://localhost:8000/v1/library/uploaded/ \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  -F "file=@/path/to/your/track.mp3"
```

The API will automatically:
- Extract metadata from the audio file
- Fingerprint the audio using AcoustID
- Match against MusicBrainz to retrieve additional metadata
- Create associated artist and album records if needed

#### 3. Create a Genre Hierarchy

```bash
# Create parent genre
curl -X POST http://localhost:8000/v1/genres/ \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Electronic Music"
  }'

# Create child genre
curl -X POST http://localhost:8000/v1/genres/ \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Techno",
    "parent": "Electronic Music"
  }'
```

When a track is tagged with "Techno", it will automatically appear in both the "Techno" and "Electronic Music" playlists.

#### 4. Tag a Track

```bash
curl -X PUT http://localhost:8000/v1/library/uploaded/{track_id}/ \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "genre": "Techno",
    "tags": ["dance", "electronic"]
  }'
```

#### 5. Search for Tracks

```bash
curl -X GET "http://localhost:8000/v1/search/?query=techno&type=track" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

#### 6. Record a Play

```bash
curl -X POST http://localhost:8000/v1/plays/ \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "track": "{track_uuid}"
  }'
```

### Advanced Features

#### Genre Tree Import

Import a complete genre hierarchy from a JSON tree structure. See the [genre tree format](data/genre_reference_tree.json) for an example.

#### Automatic Playlist Generation

Genre and tag playlists are automatically generated based on your track classifications. When you tag a track with a genre or tag, it automatically appears in the corresponding playlist.

#### MusicBrainz Integration

When uploading tracks, the API automatically:
1. Fingerprints the audio using Chromaprint
2. Matches against AcoustID database
3. Retrieves metadata from MusicBrainz
4. Populates track, artist, and album information

For more details, see the [MusicBrainz Integration documentation](api/utils/musicbrainz/README.md).

### Error Handling

The API uses standard HTTP status codes:

- `200 OK`: Successful request
- `201 Created`: Resource created successfully
- `400 Bad Request`: Invalid request data
- `401 Unauthorized`: Authentication required or invalid token
- `403 Forbidden`: Insufficient permissions
- `404 Not Found`: Resource not found
- `500 Internal Server Error`: Server error

Error responses follow this format:

```json
{
  "detail": "Error message",
  "code": "error_code"
}
```

For validation errors:

```json
{
  "field_name": [
    {
      "message": "Error message",
      "code": "error_code"
    }
  ]
}
```

## Technical Details

### Audio Metadata Handling

The HearTheMusicTree API uses [`audiometa-python`](https://github.com/your-username/audiometa-python) for reading and writing audio metadata. The implementation is format-agnostic and handles multiple metadata formats (ID3v1, ID3v2, Vorbis, RIFF) automatically. For more details, see the [Audio Metadata Handling documentation](api/utils/audiometa_adapter/README.md).

### MusicBrainz Integration

The HearTheMusicTree API integrates with MusicBrainz through the AcoustID fingerprinting service to automatically identify audio tracks and retrieve metadata such as title, artist, and release date. Audio files are fingerprinted using Chromaprint and matched against the MusicBrainz database. For more details, see the [MusicBrainz Integration documentation](api/utils/musicbrainz/README.md).

### Shared Reference Data (TMTA System User)

HearTheMusicTree uses a dedicated **TMTA system user** (username: `tmta`) to manage shared reference data visible to all users.

> **Note:** TMTA stands for "TheMusicTreeAPI" — the authoritative source for genre hierarchies and metadata in the BehindTheMusicTree ecosystem.

## Contributing

Contributions are welcome! Please read our [Contributing Guidelines](CONTRIBUTING.md) for details on our code of conduct and the process for submitting pull requests.

## License
This project is licensed under the Apache License 2.0. See the [LICENSE](LICENSE) file for details.

## Acknowledgements
This project use acoustid to fingerprint the audio files in order to identify each track.
Please visit [Acoustid Web Service](https://acoustid.org/webservice).
