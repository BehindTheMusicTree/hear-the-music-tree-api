
from rest_framework import serializers

from api.model.uploaded_track.UploadedTrack import UploadedTrack
from api.serializer.model.artist.minimum import ArtistMinimumSerializer
from api.serializer.model.criteria.output.minimum import CriteriaMinimumSerializer
from api.serializer.model.uploaded_track.output.UploadedTrackOutputFieldKey import UploadedTrackOutputFieldKey


class UploadedTrackSimpleWithoutPlaylistAndAlbumSerializer(serializers.ModelSerializer):
    artists = ArtistMinimumSerializer(many=True)
    genre = CriteriaMinimumSerializer()

    class Meta:
        model = UploadedTrack
        fields = [UploadedTrackOutputFieldKey.UUID.value,
                  UploadedTrackOutputFieldKey.TITLE.value,
                  UploadedTrackOutputFieldKey.ARTISTS.value,
                  UploadedTrackOutputFieldKey.GENRE.value,
                  UploadedTrackOutputFieldKey.RATING.value,
                  UploadedTrackOutputFieldKey.LANGUAGE.value,
                  UploadedTrackOutputFieldKey.PLAY_COUNT.value]
