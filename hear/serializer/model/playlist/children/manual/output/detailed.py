from drf_spectacular.utils import extend_schema_field
from rest_framework import serializers
from rest_framework.utils.serializer_helpers import ReturnList
from the_music_tree_api_kit.serializer.EagerLoadingMixin import EagerLoadingMixin
from the_music_tree_api_kit.serializer.field.AppCharField import AppCharField

from hear.model.playlist.children.manual.ManualPlaylist import ManualPlaylist
from hear.model.playlist.PlaylistUploadedTracks import (
    UPLOADED_TRACKS_ARCHIVED_COUNT_ANNOTATED,
    UPLOADED_TRACKS_COUNT_ANNOTATED,
    get_uploaded_tracks,
    uploaded_tracks_count_annotation,
)
from hear.serializer.model.uploaded_track.output.simple.simple_without_album import (
    UploadedTrackSimpleWithoutPlaylistAndAlbumSerializer,
)

from .Fields import Fields


class ManualPlaylistDetailedSerializer(EagerLoadingMixin, serializers.ModelSerializer):
    uploaded_tracks_count = serializers.IntegerField(source=UPLOADED_TRACKS_COUNT_ANNOTATED)
    uploaded_tracks = serializers.SerializerMethodField()
    uploaded_tracks_archived_count = serializers.IntegerField(source=UPLOADED_TRACKS_ARCHIVED_COUNT_ANNOTATED)
    name = AppCharField()

    @classmethod
    def setup_queryset(cls, queryset, prefix=""):  # noqa: ARG003 - annotations only apply to the top-level queryset
        return queryset.annotate(
            **{
                UPLOADED_TRACKS_COUNT_ANNOTATED: uploaded_tracks_count_annotation(archived=False),
                UPLOADED_TRACKS_ARCHIVED_COUNT_ANNOTATED: uploaded_tracks_count_annotation(archived=True),
            }
        )

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
            get_uploaded_tracks(obj, archived=False).select_related("genre").prefetch_related("artists"),
            many=True,
            context=self.context,
        ).data
