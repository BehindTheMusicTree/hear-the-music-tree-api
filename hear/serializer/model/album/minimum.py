from rest_framework import serializers
from the_music_tree_api_kit.serializer.AppInputSerializer import AppInputSerializer

from hear.model.album.Album import Album
from hear.serializer.model.album.Fields import Fields as AvailableFields
from hear.serializer.model.artist.minimum import ArtistMinimumSerializer


class Fields:
    UUID = AvailableFields.UUID
    NAME = AvailableFields.NAME_PUBLIC
    ALBUM_ARTISTS = AvailableFields.ALBUM_ARTISTS


class AlbumMinimumSerializer(AppInputSerializer, serializers.ModelSerializer):
    album_artists = ArtistMinimumSerializer(many=True)

    class Meta:
        model = Album
        fields = [Fields.UUID, Fields.NAME, Fields.ALBUM_ARTISTS]
