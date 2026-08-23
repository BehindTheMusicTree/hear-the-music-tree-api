from rest_framework import serializers
from the_music_tree_genre_kit.playlist.Playlist import Playlist

from hear.model.playlist.PlaylistDuration import get_duration_in_sec
from hear.serializer.model.playlist.base.output.Fields import Fields as PlayListFields
from hear.serializer.model.playlist.base.output.simple import PlaylistSimpleSerializer


class Fields:
    UUID = PlayListFields.UUID
    NAME = PlayListFields.NAME
    CREATED_ON = PlayListFields.CREATED_ON
    UPDATED_ON = PlayListFields.UPDATED_ON
    UPLOADED_TRACKS_NOT_ARCHIVED_INTERNAL = PlayListFields.UPLOADED_TRACKS_NOT_ARCHIVED_INTERNAL
    UPLOADED_TRACKS_NOT_ARCHIVED_PUBLIC = PlayListFields.UPLOADED_TRACKS_NOT_ARCHIVED_PUBLIC
    UPLOADED_TRACKS_NOT_ARCHIVED_COUNT_INTERNAL = PlayListFields.UPLOADED_TRACKS_NOT_ARCHIVED_COUNT_INTERNAL
    UPLOADED_TRACKS_NOT_ARCHIVED_COUNT_PUBLIC = PlayListFields.UPLOADED_TRACKS_NOT_ARCHIVED_COUNT_PUBLIC
    UPLOADED_TRACK_PLAYLIST_RELS_INTERNAL = PlayListFields.UPLOADED_TRACK_PLAYLIST_RELS_INTERNAL
    UPLOADED_TRACK_PLAYLIST_RELS_PUBLIC = PlayListFields.UPLOADED_TRACK_PLAYLIST_RELS_PUBLIC
    UPLOADED_TRACKS_ARCHIVED_COUNT_INTERNAL = PlayListFields.UPLOADED_TRACKS_ARCHIVED_COUNT_INTERNAL
    UPLOADED_TRACKS_ARCHIVED_COUNT_PUBLIC = PlayListFields.UPLOADED_TRACKS_ARCHIVED_COUNT_PUBLIC
    DURATION_IN_SEC = PlayListFields.DURATION_IN_SEC
    DURATION_STR_IN_HOUR_MIN_SEC = PlayListFields.DURATION_STR_IN_HOUR_MIN_SEC


class ChildPlaylistSerializer(PlaylistSimpleSerializer):
    uploaded_tracks_count = serializers.IntegerField(source=Fields.UPLOADED_TRACKS_NOT_ARCHIVED_COUNT_INTERNAL)
    uploaded_tracks = serializers.ListField(source=Fields.UPLOADED_TRACKS_NOT_ARCHIVED_INTERNAL)
    uploaded_tracks_archived_count = serializers.IntegerField(source=Fields.UPLOADED_TRACKS_ARCHIVED_COUNT_INTERNAL)
    duration_in_sec = serializers.SerializerMethodField()

    class Meta:
        model = Playlist
        fields = [
            Fields.UUID,
            Fields.CREATED_ON,
            Fields.UPDATED_ON,
            Fields.NAME,
            Fields.UPLOADED_TRACKS_NOT_ARCHIVED_COUNT_PUBLIC,
            Fields.UPLOADED_TRACKS_NOT_ARCHIVED_PUBLIC,
            Fields.UPLOADED_TRACKS_ARCHIVED_COUNT_PUBLIC,
            Fields.DURATION_IN_SEC,
            Fields.DURATION_STR_IN_HOUR_MIN_SEC,
        ]

    def get_duration_in_sec(self, obj: Playlist) -> int:
        return get_duration_in_sec(obj)
