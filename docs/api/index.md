# API Resources Index

This index lists all API resources with their base URLs, authentication requirements, and links to detailed documentation.

The path prefix is the **major version** only (e.g. `v1`), derived from `APP_VERSION`. Example: with `APP_VERSION=1.2.3`, use `v1/` in paths.

| Resource                  | Base URL                                          | Authentication | Permissions | Link                                    |
|---------------------------|---------------------------------------------------|----------------|-------------|-----------------------------------------|
| Users                     | `/v1/users/`                       | TODO           | IsAdminUser | [users.md](users.md)                   |
| Spotify profile (me)      | `/v1/me/spotify/`                  | Authenticated  | TODO        | [me_spotify.md](me_spotify.md)         |
| Library Uploaded           | `/v1/me/library/uploaded/`, `/v1/reference/library/uploaded/` | Required / Optional | Uploaded tracks owned by authenticated user or system reference | [library_uploaded.md](library_uploaded.md) |
| Library Spotify           | `/v1/me/library/spotify/` | Required | Spotify tracks in authenticated user's library | [library_spotify.md](library_spotify.md) |
| Spotify Artists           | `/v1/spotify-artists/`             | TODO           | TODO        | [spotify_artists.md](spotify_artists.md) |
| Artists                   | `/v1/artists/`                     | TODO           | TODO        | [artists.md](artists.md)                |
| Albums                    | `/v1/me/albums/`, `/v1/reference/albums/` | Required / Optional | Albums in authenticated user's library or system reference | [albums.md](albums.md) |
| Tags                      | `/v1/me/tags/`, `/v1/reference/tags/` | Required / Optional | Tags owned by authenticated user or system reference | [tags.md](tags.md)                      |
| Genres                 | `/v1/me/genres/`, `/v1/reference/genres/` | Required / Optional | Genres owned by authenticated user or system reference | [genres.md](genres.md) |
| Plays                     | `/v1/me/plays/`, `/v1/reference/plays/` | Required / Optional | Play history for authenticated user or system reference | [plays.md](plays.md)                    |
| Playlists                 | `/v1/me/playlists/`, `/v1/reference/playlists/` | Required / Optional | Playlists owned by authenticated user or system reference | [playlists.md](playlists.md)            |
| Manual Playlists          | `/v1/me/manual-playlists/`, `/v1/reference/manual-playlists/` | Required / Optional | Manual playlists owned by authenticated user or system reference | [manual_playlists.md](manual_playlists.md) |
| Genre Playlists        | `/v1/me/genre-playlists/`, `/v1/reference/genre-playlists/` | Required / Optional | Genre playlists owned by authenticated user or system reference | [genre_playlists.md](genre_playlists.md) |
| Reference Genres          | `/v1/reference/genres/`             | None           | None        | [reference_genres.md](reference_genres.md) |
| Tag Playlists             | `/v1/me/tag-playlists/`, `/v1/reference/tag-playlists/` | Required / Optional | Tag playlists owned by authenticated user or system reference | [tag_playlists.md](tag_playlists.md)     |
| All Tracks                | `/v1/all-tracks/`                  | TODO           | TODO        | [all_tracks.md](all_tracks.md)           |
| Search                    | `/v1/search/`                      | TODO           | TODO        | [search.md](search.md)                   |
| Audio metadata (read raw) | `/v1/audio/metadata/full/`        | None           | Public      | [audio_metadata.md](audio_metadata.md)  |
| Metadata session (session + download) | `/v1/audio/metadata/session/`, `/v1/audio/metadata/session-download/` | None | Public | [audio_metadata_session.md](audio_metadata_session.md) |