from rest_framework import serializers

from hear.model.uploaded_track.UploadedTrack import UploadedTrack
from hear.serializer.model.artist.minimum import ArtistMinimumSerializer

from .UploadedTrackOutputFieldKey import UploadedTrackOutputFieldKey


class UploadedTrackMinimumSerializer(serializers.ModelSerializer):
    artists = ArtistMinimumSerializer(many=True)

    class Meta:
        model = UploadedTrack
        fields = [
            UploadedTrackOutputFieldKey.UUID.value,
            UploadedTrackOutputFieldKey.TITLE.value,
            UploadedTrackOutputFieldKey.ARTISTS.value,
        ]
