from the_music_tree_api_kit.public_standard_resource.Fields import Fields as PublicStandardResourceFields

from api.model.spotify_resource.children.artist.Fields import Fields as SpotifyArtistFields


class Fields:
    SPOTIFY_ID = SpotifyArtistFields.SPOTIFY_ID
    NAME = SpotifyArtistFields.NAME
    POPULARITY = SpotifyArtistFields.POPULARITY
    SPOTIFY_LINK = SpotifyArtistFields.SPOTIFY_LINK
    GENRES = SpotifyArtistFields.GENRES
    IMAGES = SpotifyArtistFields.IMAGES
    CREATED_ON = PublicStandardResourceFields.CREATED_ON
    UPDATED_ON = PublicStandardResourceFields.UPDATED_ON
