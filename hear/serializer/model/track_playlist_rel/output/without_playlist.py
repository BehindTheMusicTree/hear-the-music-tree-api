from rest_framework import serializers
from the_music_tree_genre_kit.criteria.track_playlist_rel.TrackPlaylistRel import TrackPlaylistRel

from hear.model.uploaded_track.UploadedTrackFieldKey import UploadedTrackFieldKey
from hear.serializer.model.uploaded_track.output.detailed import UploadedTrackDetailedSerializer

from .Fields import Fields


class TrackPlaylistRelWithoutPlaylist(serializers.ModelSerializer):
    track = UploadedTrackDetailedSerializer(
        source=f"{Fields.TRACK_INTERNAL}.{UploadedTrackFieldKey.UPLOADED_TRACK_RELATED_NAME.value}"
    )

    class Meta:
        model = TrackPlaylistRel
        fields = [
            Fields.TRACK_PUBLIC,
            Fields.POSITION,
        ]
