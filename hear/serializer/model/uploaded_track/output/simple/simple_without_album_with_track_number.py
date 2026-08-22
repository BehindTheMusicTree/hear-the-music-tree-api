from rest_framework import serializers

from hear.model.uploaded_track.UploadedTrack import UploadedTrack
from hear.serializer.model.artist.minimum import ArtistMinimumSerializer
from hear.serializer.model.criteria.output.minimum import CriteriaMinimumSerializer

from ..UploadedTrackOutputFieldKey import UploadedTrackOutputFieldKey


class UploadedTrackSimpleWithoutAlbumWithPositionInAlbumSerializer(serializers.ModelSerializer):
    genre = CriteriaMinimumSerializer()
    artists = ArtistMinimumSerializer(many=True)

    class Meta:
        model = UploadedTrack
        fields = [
            UploadedTrackOutputFieldKey.UUID.value,
            UploadedTrackOutputFieldKey.TITLE.value,
            UploadedTrackOutputFieldKey.ARTISTS.value,
            UploadedTrackOutputFieldKey.TRACK_NUMBER.value,
            UploadedTrackOutputFieldKey.GENRE.value,
            UploadedTrackOutputFieldKey.RATING.value,
            UploadedTrackOutputFieldKey.LANGUAGE.value,
            UploadedTrackOutputFieldKey.PLAY_COUNT.value,
        ]
