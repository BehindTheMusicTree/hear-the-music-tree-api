from rest_framework import serializers
from the_music_tree_api_kit.serializer.AppInputSerializer import AppInputSerializer

from api.model.playlist.Fields import Fields as PlayListFields
from api.model.playlist.Playlist import Playlist


class Fields:
    USER = PlayListFields.USER


class PlaylistModelSerializer(AppInputSerializer, serializers.ModelSerializer):
    class Meta:
        model = Playlist
        fields = [Fields.USER]
