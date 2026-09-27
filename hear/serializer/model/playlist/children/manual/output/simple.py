from rest_framework import serializers
from the_music_tree_api_kit.serializer.field.AppCharField import AppCharField

from hear.model.playlist.children.manual.ManualPlaylist import ManualPlaylist
from hear.serializer.model.playlist.base.output.UploadedTracksCountsMixin import UploadedTracksCountsMixin

from .Fields import Fields as AvailableFields


class Fields:
    UUID = AvailableFields.UUID
    NAME = AvailableFields.NAME
    UPLOADED_TRACKS_NOT_ARCHIVED_COUNT_PUBLIC = AvailableFields.UPLOADED_TRACKS_NOT_ARCHIVED_COUNT_PUBLIC
    CREATED_ON = AvailableFields.CREATED_ON


class ManualPlaylistSimpleSerializer(UploadedTracksCountsMixin, serializers.ModelSerializer):
    name = AppCharField()
    uploaded_tracks_count = serializers.SerializerMethodField()

    class Meta:
        model = ManualPlaylist
        fields = [Fields.UUID, Fields.NAME, Fields.UPLOADED_TRACKS_NOT_ARCHIVED_COUNT_PUBLIC, Fields.CREATED_ON]
