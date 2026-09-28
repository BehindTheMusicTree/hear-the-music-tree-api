from django.db.models import Prefetch
from rest_framework import serializers
from the_music_tree_api_kit.serializer.EagerLoadingMixin import EagerLoadingMixin
from the_music_tree_api_kit.serializer.field.AppCharField import AppCharField
from the_music_tree_genre_kit.criteria.track_playlist_rel.TrackPlaylistRel import TrackPlaylistRel
from the_music_tree_genre_kit.playlist.Playlist import Playlist

from hear.model.playlist.PlaylistDuration import format_duration_in_hour_min_sec
from hear.model.playlist.PlaylistUploadedTracks import (
    DURATION_IN_SEC_ANNOTATED,
    UPLOADED_TRACKS_ARCHIVED_COUNT_ANNOTATED,
    UPLOADED_TRACKS_COUNT_ANNOTATED,
    duration_in_sec_annotation,
    uploaded_tracks_count_annotation,
)
from hear.serializer.model.playlist.base.output.minimum import PlaylistMinimumSerializer
from hear.serializer.model.track_playlist_rel.output.without_playlist import (
    TrackPlaylistRelWithoutPlaylist,
)

from .Fields import Fields


def annotate_counts_and_duration(queryset):
    return queryset.annotate(
        **{
            UPLOADED_TRACKS_COUNT_ANNOTATED: uploaded_tracks_count_annotation(archived=False),
            UPLOADED_TRACKS_ARCHIVED_COUNT_ANNOTATED: uploaded_tracks_count_annotation(archived=True),
            DURATION_IN_SEC_ANNOTATED: duration_in_sec_annotation(),
        }
    )


def prefetch_uploaded_track_playlist_rels(queryset):
    return queryset.prefetch_related(
        Prefetch(
            Fields.UPLOADED_TRACK_PLAYLIST_RELS_INTERNAL,
            queryset=TrackPlaylistRelWithoutPlaylist.setup_queryset(TrackPlaylistRel._default_manager.all()),
        )
    )


class PlaylistDetailedSerializer(EagerLoadingMixin, serializers.ModelSerializer):
    uploaded_track_playlist_relations = TrackPlaylistRelWithoutPlaylist(
        source=Fields.UPLOADED_TRACK_PLAYLIST_RELS_INTERNAL, many=True
    )
    uploaded_tracks_count = serializers.IntegerField(source=UPLOADED_TRACKS_COUNT_ANNOTATED)
    uploaded_tracks_archived_count = serializers.IntegerField(source=UPLOADED_TRACKS_ARCHIVED_COUNT_ANNOTATED)
    type = AppCharField(source=Fields.TYPE_LABEL_INTERNAL)
    duration_in_sec = serializers.IntegerField(source=DURATION_IN_SEC_ANNOTATED)
    duration_str_in_hour_min_sec = serializers.SerializerMethodField()

    @classmethod
    def setup_queryset(cls, queryset, prefix=""):
        return PlaylistMinimumSerializer.setup_queryset(
            prefetch_uploaded_track_playlist_rels(annotate_counts_and_duration(queryset)), prefix
        )

    class Meta:
        model = Playlist
        fields = [
            Fields.UUID,
            Fields.NAME,
            Fields.TYPE_LABEL_PUBLIC,
            Fields.UPLOADED_TRACKS_NOT_ARCHIVED_COUNT_PUBLIC,
            Fields.UPLOADED_TRACK_PLAYLIST_RELS_PUBLIC,
            Fields.UPLOADED_TRACKS_ARCHIVED_COUNT_PUBLIC,
            Fields.DURATION_IN_SEC,
            Fields.DURATION_STR_IN_HOUR_MIN_SEC,
            Fields.PLAY_COUNT,
            Fields.CREATED_ON,
            Fields.UPDATED_ON,
        ]

    def get_duration_str_in_hour_min_sec(self, obj: Playlist) -> str:
        return format_duration_in_hour_min_sec(getattr(obj, DURATION_IN_SEC_ANNOTATED))
