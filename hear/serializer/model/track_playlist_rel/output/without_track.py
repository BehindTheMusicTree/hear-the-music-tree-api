from rest_framework import serializers
from the_music_tree_genre_kit.criteria.track_playlist_rel.TrackPlaylistRel import TrackPlaylistRel

from hear.serializer.model.playlist.base.output.minimum import PlaylistMinimumSerializer

from .Fields import Fields


class TrackPlaylistRelWithoutTrack(serializers.ModelSerializer):
    playlist = PlaylistMinimumSerializer()

    class Meta:
        model = TrackPlaylistRel
        fields = [Fields.PLAYLIST, Fields.POSITION]
