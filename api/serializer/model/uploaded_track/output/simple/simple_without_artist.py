from rest_framework import serializers
from the_music_tree_genre_kit.serializer.model.criteria.output.minimum import CriteriaMinimumSerializer

from api.model.uploaded_track.UploadedTrack import UploadedTrack
from api.serializer.model.album.minimum import AlbumMinimumSerializer
from api.serializer.model.uploaded_track.output.UploadedTrackOutputFieldKey import UploadedTrackOutputFieldKey


class UploadedTrackSimpleWithoutPlaylistAndArtistSerializer(serializers.ModelSerializer):
    album = AlbumMinimumSerializer()
    genre = CriteriaMinimumSerializer()

    class Meta:
        model = UploadedTrack
        fields = [
            UploadedTrackOutputFieldKey.UUID.value,
            UploadedTrackOutputFieldKey.TITLE.value,
            UploadedTrackOutputFieldKey.ALBUM.value,
            UploadedTrackOutputFieldKey.GENRE.value,
            UploadedTrackOutputFieldKey.RATING.value,
            UploadedTrackOutputFieldKey.LANGUAGE.value,
            UploadedTrackOutputFieldKey.PLAY_COUNT.value,
        ]
