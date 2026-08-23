from rest_framework import serializers

from hear.model.playlist.children.criteria.CriteriaPlaylist import CriteriaPlaylist
from hear.model.playlist.PlaylistDuration import get_duration_in_sec, get_duration_str_in_hour_min_sec
from hear.serializer.model.criteria.output.minimum import CriteriaMinimumSerializer
from hear.serializer.model.playlist.children.criteria.output.minumum import CriteriaPlaylistMinimumSerializer
from hear.serializer.model.track_playlist_rel.output.without_playlist import (
    TrackPlaylistRelWithoutPlaylist,
)

from .Fields import Fields


class CriteriaPlaylistDetailedSerializer(serializers.ModelSerializer):
    uploaded_track_playlist_relations = TrackPlaylistRelWithoutPlaylist(
        source=Fields.UPLOADED_TRACK_PLAYLIST_RELS_INTERNAL, many=True
    )
    uploaded_tracks_count = serializers.IntegerField(source=Fields.UPLOADED_TRACKS_NOT_ARCHIVED_COUNT_INTERNAL)
    uploaded_tracks_archived_count = serializers.IntegerField(source=Fields.UPLOADED_TRACKS_ARCHIVED_COUNT_INTERNAL)
    criteria = CriteriaMinimumSerializer()
    root = CriteriaPlaylistMinimumSerializer()  # type: ignore
    parent = CriteriaPlaylistMinimumSerializer()
    duration_in_sec = serializers.SerializerMethodField()
    duration_str_in_hour_min_sec = serializers.SerializerMethodField()

    class Meta:
        model = CriteriaPlaylist
        fields = [
            Fields.UUID,
            Fields.NAME,
            Fields.UPLOADED_TRACK_PLAYLIST_RELS_PUBLIC,
            Fields.UPLOADED_TRACKS_NOT_ARCHIVED_COUNT_PUBLIC,
            Fields.DURATION_IN_SEC,
            Fields.DURATION_STR_IN_HOUR_MIN_SEC,
            Fields.UPLOADED_TRACKS_ARCHIVED_COUNT_PUBLIC,
            Fields.CRITERIA,
            Fields.PARENT,
            Fields.ROOT,
            Fields.CREATED_ON,
            Fields.UPDATED_ON,
        ]

    def get_duration_in_sec(self, obj: CriteriaPlaylist) -> int:
        return get_duration_in_sec(obj)

    def get_duration_str_in_hour_min_sec(self, obj: CriteriaPlaylist) -> str:
        return get_duration_str_in_hour_min_sec(obj)
