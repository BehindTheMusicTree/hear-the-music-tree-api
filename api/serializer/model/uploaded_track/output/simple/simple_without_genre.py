from rest_framework import serializers

from api.model.uploaded_track.UploadedTrack import UploadedTrack
from api.serializer.model.album.minimum import AlbumMinimumSerializer
from api.serializer.model.artist.minimum import ArtistMinimumSerializer
from api.serializer.model.uploaded_track.output.UploadedTrackOutputFieldKey import UploadedTrackOutputFieldKey


class UploadedTrackSimpleWithoutGenreSerializer(serializers.ModelSerializer):
    artists = ArtistMinimumSerializer(many=True)
    album = AlbumMinimumSerializer()

    class Meta:
        model = UploadedTrack
        fields = [
            UploadedTrackOutputFieldKey.UUID.value,
            UploadedTrackOutputFieldKey.TITLE.value,
            UploadedTrackOutputFieldKey.ARTISTS.value,
            UploadedTrackOutputFieldKey.ALBUM.value,
            UploadedTrackOutputFieldKey.RATING.value,
            UploadedTrackOutputFieldKey.LANGUAGE.value,
            UploadedTrackOutputFieldKey.PLAY_COUNT.value,
        ]
