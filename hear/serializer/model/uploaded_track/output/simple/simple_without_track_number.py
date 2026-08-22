from rest_framework import serializers

from hear.model.uploaded_track.UploadedTrack import UploadedTrack
from hear.serializer.model.album.minimum import AlbumMinimumSerializer
from hear.serializer.model.artist.minimum import ArtistMinimumSerializer
from hear.serializer.model.criteria.output.minimum import CriteriaMinimumSerializer
from hear.serializer.model.uploaded_track.output.UploadedTrackOutputFieldKey import UploadedTrackOutputFieldKey


class UploadedTrackSimpleWithoutPositionInAlbumSerializer(serializers.ModelSerializer):
    artists = ArtistMinimumSerializer(many=True)
    album = AlbumMinimumSerializer()
    genre = CriteriaMinimumSerializer()

    class Meta:
        model = UploadedTrack
        fields = [
            UploadedTrackOutputFieldKey.UUID.value,
            UploadedTrackOutputFieldKey.TITLE.value,
            UploadedTrackOutputFieldKey.ARTISTS.value,
            UploadedTrackOutputFieldKey.ALBUM.value,
            UploadedTrackOutputFieldKey.GENRE.value,
            UploadedTrackOutputFieldKey.RATING.value,
            UploadedTrackOutputFieldKey.LANGUAGE.value,
            UploadedTrackOutputFieldKey.PLAY_COUNT.value,
        ]
