from rest_framework import serializers
from the_music_tree_api_kit.serializer.EagerLoadingMixin import EagerLoadingMixin
from the_music_tree_api_kit.serializer.field.AppCharField import AppCharField

from hear.model.playlist.children.manual.ManualPlaylist import ManualPlaylist
from hear.model.playlist.PlaylistUploadedTracks import UPLOADED_TRACKS_COUNT_ANNOTATED, uploaded_tracks_count_annotation

from .Fields import Fields as AvailableFields


class Fields:
    UUID = AvailableFields.UUID
    NAME = AvailableFields.NAME
    UPLOADED_TRACKS_NOT_ARCHIVED_COUNT_PUBLIC = AvailableFields.UPLOADED_TRACKS_NOT_ARCHIVED_COUNT_PUBLIC
    CREATED_ON = AvailableFields.CREATED_ON


class ManualPlaylistSimpleSerializer(EagerLoadingMixin, serializers.ModelSerializer):
    name = AppCharField()
    uploaded_tracks_count = serializers.IntegerField(source=UPLOADED_TRACKS_COUNT_ANNOTATED)

    @classmethod
    def setup_queryset(cls, queryset, prefix=""):  # noqa: ARG003 - annotations only apply to the top-level queryset
        return queryset.annotate(**{UPLOADED_TRACKS_COUNT_ANNOTATED: uploaded_tracks_count_annotation(archived=False)})

    class Meta:
        model = ManualPlaylist
        fields = [Fields.UUID, Fields.NAME, Fields.UPLOADED_TRACKS_NOT_ARCHIVED_COUNT_PUBLIC, Fields.CREATED_ON]
