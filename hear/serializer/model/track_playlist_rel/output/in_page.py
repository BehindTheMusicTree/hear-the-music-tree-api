from rest_framework import serializers
from the_music_tree_api_kit.serializer.EagerLoadingMixin import EagerLoadingMixin
from the_music_tree_genre_kit.criteria.track_playlist_rel.TrackPlaylistRel import TrackPlaylistRel

from hear.model.uploaded_track.UploadedTrackFieldKey import UploadedTrackFieldKey
from hear.serializer.model.uploaded_track.output.without_playlists import UploadedTrackWithoutPlaylistsSerializer

from .Fields import Fields


class TrackPlaylistRelInPageSerializer(EagerLoadingMixin, serializers.ModelSerializer):
    track = UploadedTrackWithoutPlaylistsSerializer(
        source=f"{Fields.TRACK_INTERNAL}.{UploadedTrackFieldKey.UPLOADED_TRACK_RELATED_NAME.value}"
    )

    @classmethod
    def setup_queryset(cls, queryset, prefix=""):
        uploaded_track = f"{prefix}{Fields.TRACK_INTERNAL}__{UploadedTrackFieldKey.UPLOADED_TRACK_RELATED_NAME.value}"
        # Archived tracks are hidden, so the page total matches the playlist's uploadedTracksCount.
        return UploadedTrackWithoutPlaylistsSerializer.setup_queryset(
            queryset.filter(**{f"{uploaded_track}__archived": False}).select_related(uploaded_track),
            prefix=f"{uploaded_track}__",
        )

    class Meta:
        model = TrackPlaylistRel
        fields = [Fields.TRACK_PUBLIC, Fields.POSITION]
