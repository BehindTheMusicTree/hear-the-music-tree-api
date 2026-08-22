from rest_framework import serializers
from the_music_tree_api_kit.serializer.AppInputSerializer import AppInputSerializer

from hear.model.uploaded_track.UploadedTrack import UploadedTrack
from hear.serializer.model.artist.minimum import ArtistMinimumSerializer
from hear.serializer.model.uploaded_track.output.UploadedTrackOutputFieldKey import UploadedTrackOutputFieldKey


class UploadedTrackWithoutAlbumPlaylistGenreSerializer(AppInputSerializer, serializers.ModelSerializer):
    artists = ArtistMinimumSerializer(many=True)

    class Meta:
        model = UploadedTrack
        fields = [
            UploadedTrackOutputFieldKey.UUID.value,
            UploadedTrackOutputFieldKey.TITLE.value,
            UploadedTrackOutputFieldKey.ARTISTS.value,
            UploadedTrackOutputFieldKey.RATING.value,
            UploadedTrackOutputFieldKey.LANGUAGE.value,
            UploadedTrackOutputFieldKey.PLAY_COUNT.value,
        ]
