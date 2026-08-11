from typing import Any

from rest_framework import serializers
from the_music_tree_api_kit.serializer.field.AppCharField import AppCharField

from api.model.play.Play import Play
from api.model.playlist.Playlist import Playlist
from api.serializer.model.playlist.base.output.detailed import PlaylistDetailedSerializer
from api.serializer.model.uploaded_track.output.detailed import UploadedTrackDetailedSerializer

from .Fields import Fields


class PlayDetailedSerializer(serializers.ModelSerializer):
    content_type = AppCharField(source=f"{Fields.CONTENT_TYPE}.model")
    content = serializers.SerializerMethodField()

    class Meta:
        model = Play
        fields = [Fields.UUID, Fields.CONTENT_TYPE, Fields.CONTENT, Fields.CREATED_ON]

    def get_content(self, obj: Play) -> list | Any | dict:
        if isinstance(obj.content, Playlist):
            return PlaylistDetailedSerializer(obj.content).data
        return UploadedTrackDetailedSerializer(obj.content).data
