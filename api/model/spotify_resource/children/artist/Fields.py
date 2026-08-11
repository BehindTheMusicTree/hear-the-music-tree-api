from the_music_tree_api_kit.public_standard_resource.Fields import Fields as PublicStandardResourceFields

from api.model.spotify_resource.Fields import Fields as SpotifyFields


class Fields(SpotifyFields, PublicStandardResourceFields):
    NAME = "name"
    POPULARITY = "popularity"
    SPOTIFY_LINK = "spotify_link"
    GENRES = "genres"
    IMAGES = "images"
