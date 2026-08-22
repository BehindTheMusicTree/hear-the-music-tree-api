from rest_framework import serializers

from hear.model.spotify_resource.children.artist.SpotifyArtist import SpotifyArtist
from hear.serializer.model.spotify.artist.output.Fields import Fields


class SpotifyArtistDetailedSerializer(serializers.ModelSerializer):
    class Meta:
        model = SpotifyArtist
        fields = [
            Fields.SPOTIFY_ID,
            Fields.NAME,
            Fields.POPULARITY,
            Fields.SPOTIFY_LINK,
            Fields.GENRES,
            Fields.IMAGES,
        ]
