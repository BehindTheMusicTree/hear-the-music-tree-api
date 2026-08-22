from rest_framework import serializers
from the_music_tree_api_kit.serializer.AppInputSerializer import AppInputSerializer

from hear.model.artist.Artist import Artist
from hear.serializer.model.album.Fields import Fields as AvailableFields


class Fields:
    UUID = AvailableFields.UUID
    NAME = AvailableFields.NAME_PUBLIC


class ArtistMinimumSerializer(AppInputSerializer, serializers.ModelSerializer):
    class Meta:
        model = Artist
        fields = [Fields.UUID, Fields.NAME]
