from rest_framework import serializers
from the_music_tree_api_kit.serializer.AppInputSerializer import AppInputSerializer

from api import settings
from api.model.playlist.children.manual.Fields import Fields as ModelFields
from api.model.playlist.children.manual.ManualPlaylist import ManualPlaylist
from api.serializer.field.UniquePerUserNameField import UniquePerUserNameField


class ManualPlaylistInputSerializer(AppInputSerializer, serializers.ModelSerializer):
    name = UniquePerUserNameField(
        model=ManualPlaylist, max_length=settings.MANUAL_PLAYLIST_NAME_LEN_MAX, allow_blank=False
    )

    class Meta:
        model = ManualPlaylist
        fields = [ModelFields.NAME_PUBLIC]
