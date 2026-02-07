# API Resources Index

This index lists all API resources with their base URLs, authentication requirements, and links to detailed documentation.

| Resource                  | Base URL                                          | Authentication | Permissions | Link                                    |
|---------------------------|---------------------------------------------------|----------------|-------------|-----------------------------------------|
| Users                     | `/api/{APP_VERSION}/users/`                       | TODO           | IsAdminUser | [users.md](users.md)                   |
| Spotify Users             | `/api/{APP_VERSION}/users/spotify/`               | Authenticated  | TODO        | [users_spotify.md](users_spotify.md)   |
| Library Uploaded           | `/api/{APP_VERSION}/me/library/uploaded/`, `/api/{APP_VERSION}/reference/library/uploaded/` | Required / Optional | Uploaded tracks owned by authenticated user or system reference | [library_uploaded.md](library_uploaded.md) |
| Library Spotify           | `/api/{APP_VERSION}/library/spotify/`             | TODO           | TODO        | [library_spotify.md](library_spotify.md) |
| Spotify Artists           | `/api/{APP_VERSION}/spotify-artists/`             | TODO           | TODO        | [spotify_artists.md](spotify_artists.md) |
| Artists                   | `/api/{APP_VERSION}/artists/`                     | TODO           | TODO        | [artists.md](artists.md)                |
| Albums                    | `/api/{APP_VERSION}/me/albums/`, `/api/{APP_VERSION}/reference/albums/` | Required / Optional | Albums in authenticated user's library or system reference | [albums.md](albums.md) |
| Tags                      | `/api/{APP_VERSION}/tags/`                        | TODO           | TODO        | [tags.md](tags.md)                      |
| Genres                 | `/api/{APP_VERSION}/me/genres/`, `/api/{APP_VERSION}/reference/genres/` | Required / Optional | Genres owned by authenticated user or system reference | [genres.md](genres.md) |
| Plays                     | `/api/{APP_VERSION}/plays/`                       | TODO           | TODO        | [plays.md](plays.md)                    |
| Playlists                 | `/api/{APP_VERSION}/playlists/`                   | TODO           | TODO        | [playlists.md](playlists.md)            |
| Manual Playlists          | `/api/{APP_VERSION}/manual-playlists/`            | TODO           | TODO        | [manual_playlists.md](manual_playlists.md) |
| Genre Playlists        | `/api/{APP_VERSION}/me/genre-playlists/`, `/api/{APP_VERSION}/reference/genre-playlists/` | Required / Optional | Genre playlists owned by authenticated user or system reference | [genre_playlists.md](genre_playlists.md) |
| Reference Genres          | `/api/{APP_VERSION}/reference/genres/`             | None           | None        | [reference_genres.md](reference_genres.md) |
| Tag Playlists             | `/api/{APP_VERSION}/tag-playlists/`               | TODO           | TODO        | [tag_playlists.md](tag_playlists.md)     |
| All Tracks                | `/api/{APP_VERSION}/all-tracks/`                  | TODO           | TODO        | [all_tracks.md](all_tracks.md)           |
| Search                    | `/api/{APP_VERSION}/search/`                      | TODO           | TODO        | [search.md](search.md)                   |