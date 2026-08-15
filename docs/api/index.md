# API Resources Index

This index lists all API resources with their base URLs, authentication requirements, and links to detailed documentation.

The path prefix is the **major version** only (e.g. `v1`), derived from `APP_VERSION`. Example: with `APP_VERSION=1.2.3`, use `v1/` in paths.

| Resource                              | Base URL                                                              | Authentication | Permissions                                    | Link                                                   |
| ------------------------------------- | --------------------------------------------------------------------- | -------------- | ---------------------------------------------- | ------------------------------------------------------ |
| Users                                 | `/v1/users/`                                                          | TODO           | IsAdminUser                                    | [users.md](users.md)                                   |
| Spotify profile (me)                  | `/v1/me/spotify/`                                                     | Authenticated  | TODO                                           | [me_spotify.md](me_spotify.md)                         |
| Library Uploaded                      | `/v1/me/library/uploaded/`                                            | Required       | Uploaded tracks owned by authenticated user    | [library_uploaded.md](library_uploaded.md)             |
| Library Spotify                       | `/v1/me/library/spotify/`                                             | Required       | Spotify tracks in authenticated user's library | [library_spotify.md](library_spotify.md)               |
| Spotify Artists                       | `/v1/spotify-artists/`                                                | TODO           | TODO                                           | [spotify_artists.md](spotify_artists.md)               |
| Artists                               | `/v1/artists/`                                                        | TODO           | TODO                                           | [artists.md](artists.md)                               |
| Albums                                | `/v1/me/albums/`                                                      | Required       | Albums in authenticated user's library         | [albums.md](albums.md)                                 |
| Tags                                  | `/v1/me/tags/`                                                        | Required       | Tags owned by authenticated user               | [tags.md](tags.md)                                     |
| Genres                                | `/v1/me/genres/`                                                      | Required       | Genres owned by authenticated user             | [genres.md](genres.md)                                 |
| Plays                                 | `/v1/me/plays/`                                                       | Required       | Play history for authenticated user            | [plays.md](plays.md)                                   |
| Playlists                             | `/v1/me/playlists/`                                                   | Required       | Playlists owned by authenticated user          | [playlists.md](playlists.md)                           |
| Manual Playlists                      | `/v1/me/manual-playlists/`                                            | Required       | Manual playlists owned by authenticated user   | [manual_playlists.md](manual_playlists.md)             |
| Genre Playlists                       | `/v1/me/genre-playlists/`                                             | Required       | Genre playlists owned by authenticated user    | [genre_playlists.md](genre_playlists.md)               |
| Tag Playlists                         | `/v1/me/tag-playlists/`                                               | Required       | Tag playlists owned by authenticated user      | [tag_playlists.md](tag_playlists.md)                   |
| All Tracks                            | `/v1/all-tracks/`                                                     | TODO           | TODO                                           | [all_tracks.md](all_tracks.md)                         |
| Search                                | `/v1/search/`                                                         | TODO           | TODO                                           | [search.md](search.md)                                 |
| Audio metadata (read raw)             | `/v1/audio/metadata/full/`                                            | None           | Public                                         | [audio_metadata.md](audio_metadata.md)                 |
| Metadata session (session + download) | `/v1/audio/metadata/session/`, `/v1/audio/metadata/session-download/` | None           | Public                                         | [audio_metadata_session.md](audio_metadata_session.md) |
