from rest_framework import serializers
from the_music_tree_genre_kit.criteria.track_playlist_rel.TrackPlaylistRel import TrackPlaylistRel

from hear.serializer.model.uploaded_track.output.detailed import UploadedTrackDetailedSerializer

from .Fields import Fields


class TrackPlaylistRelWithoutPlaylist(serializers.ModelSerializer):
    track = UploadedTrackDetailedSerializer()

    class Meta:
        model = TrackPlaylistRel
        fields = [
            Fields.TRACK_PUBLIC,
            Fields.POSITION,
        ]
