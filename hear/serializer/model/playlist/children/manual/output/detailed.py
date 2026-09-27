from drf_spectacular.utils import extend_schema_field
from rest_framework import serializers
from rest_framework.utils.serializer_helpers import ReturnList
from the_music_tree_api_kit.serializer.field.AppCharField import AppCharField

from hear.model.playlist.children.manual.ManualPlaylist import ManualPlaylist
from hear.model.playlist.PlaylistUploadedTracks import get_uploaded_tracks
from hear.serializer.model.playlist.base.output.UploadedTracksCountsMixin import UploadedTracksCountsMixin
from hear.serializer.model.uploaded_track.output.simple.simple_without_album import (
    UploadedTrackSimpleWithoutPlaylistAndAlbumSerializer,
)

from .Fields import Fields


class ManualPlaylistDetailedSerializer(UploadedTracksCountsMixin, serializers.ModelSerializer):
    uploaded_tracks_count = serializers.SerializerMethodField()
    uploaded_tracks = serializers.SerializerMethodField()
    uploaded_tracks_archived_count = serializers.SerializerMethodField()
    name = AppCharField()

    class Meta:
        model = ManualPlaylist
        fields = [
            Fields.UUID,
            Fields.NAME,
            Fields.UPLOADED_TRACKS_NOT_ARCHIVED_PUBLIC,
            Fields.UPLOADED_TRACKS_NOT_ARCHIVED_COUNT_PUBLIC,
            Fields.UPLOADED_TRACKS_ARCHIVED_COUNT_PUBLIC,
            Fields.CREATED_ON,
            Fields.UPDATED_ON,
        ]

    @extend_schema_field(UploadedTrackSimpleWithoutPlaylistAndAlbumSerializer(many=True))
    def get_uploaded_tracks(self, obj: ManualPlaylist) -> ReturnList:
        return UploadedTrackSimpleWithoutPlaylistAndAlbumSerializer(
            get_uploaded_tracks(obj, archived=False), many=True, context=self.context
        ).data
