from rest_framework import serializers
from the_music_tree_api_kit.serializer.EagerLoadingMixin import EagerLoadingMixin
from the_music_tree_api_kit.serializer.field.AppCharField import AppCharField
from the_music_tree_genre_kit.playlist.Playlist import Playlist

from hear.model.playlist.PlaylistDuration import format_duration_in_hour_min_sec
from hear.model.playlist.PlaylistUploadedTracks import (
    DURATION_IN_SEC_ANNOTATED,
    UPLOADED_TRACKS_COUNT_ANNOTATED,
    duration_in_sec_annotation,
    uploaded_tracks_count_annotation,
)
from hear.serializer.model.playlist.base.output.Fields import Fields as AvailableFields
from hear.serializer.model.playlist.base.output.minimum import PlaylistMinimumSerializer


class Fields:
    UUID = AvailableFields.UUID
    UPLOADED_TRACKS_NOT_ARCHIVED_COUNT_PUBLIC = AvailableFields.UPLOADED_TRACKS_NOT_ARCHIVED_COUNT_PUBLIC
    DURATION_STR_IN_HOUR_MIN_SEC = AvailableFields.DURATION_STR_IN_HOUR_MIN_SEC
    NAME = AvailableFields.NAME
    TYPE_LABEL_INTERNAL = AvailableFields.TYPE_LABEL_INTERNAL
    TYPE_LABEL_PUBLIC = AvailableFields.TYPE_LABEL_PUBLIC
    CREATED_ON = AvailableFields.CREATED_ON


class PlaylistSimpleSerializer(EagerLoadingMixin, serializers.ModelSerializer):
    type = AppCharField(source=Fields.TYPE_LABEL_INTERNAL)
    uploaded_tracks_count = serializers.IntegerField(source=UPLOADED_TRACKS_COUNT_ANNOTATED)
    duration_str_in_hour_min_sec = serializers.SerializerMethodField()

    @classmethod
    def setup_queryset(cls, queryset, prefix=""):
        return PlaylistMinimumSerializer.setup_queryset(queryset, prefix).annotate(
            **{
                UPLOADED_TRACKS_COUNT_ANNOTATED: uploaded_tracks_count_annotation(archived=False),
                DURATION_IN_SEC_ANNOTATED: duration_in_sec_annotation(),
            }
        )

    class Meta:
        model = Playlist
        fields = [
            Fields.UUID,
            Fields.NAME,
            Fields.TYPE_LABEL_PUBLIC,
            Fields.UPLOADED_TRACKS_NOT_ARCHIVED_COUNT_PUBLIC,
            Fields.DURATION_STR_IN_HOUR_MIN_SEC,
            Fields.CREATED_ON,
        ]

    def get_duration_str_in_hour_min_sec(self, obj: Playlist) -> str:
        return format_duration_in_hour_min_sec(getattr(obj, DURATION_IN_SEC_ANNOTATED))
