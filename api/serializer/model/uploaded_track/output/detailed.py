from rest_framework import serializers
from the_music_tree_genre_kit.serializer.model.criteria.output.minimum import CriteriaMinimumSerializer

from api.model.uploaded_track.UploadedTrack import UploadedTrack
from api.model.uploaded_track.UploadedTrackFieldKey import UploadedTrackFieldKey as ModelFields
from api.serializer.model.album.minimum import AlbumMinimumSerializer
from api.serializer.model.artist.minimum import ArtistMinimumSerializer
from api.serializer.model.playlist.base.output.minimum import PlaylistMinimumSerializer
from api.serializer.model.uploaded_track.output.UploadedTrackOutputFieldKey import UploadedTrackOutputFieldKey
from api.serializer.model.uploaded_track_file.output.detailed import FileDetailedSerializer


class UploadedTrackDetailedSerializer(serializers.ModelSerializer):
    file = FileDetailedSerializer(source=ModelFields.TRACK_FILE_INTERNAL.value)
    artists = ArtistMinimumSerializer(many=True)
    album = AlbumMinimumSerializer()
    genre = CriteriaMinimumSerializer()
    playlists = PlaylistMinimumSerializer(many=True)

    class Meta:
        model = UploadedTrack
        fields = [
            UploadedTrackOutputFieldKey.UUID.value,
            UploadedTrackOutputFieldKey.RELATIVE_URL.value,
            UploadedTrackOutputFieldKey.TITLE.value,
            UploadedTrackOutputFieldKey.FILE.value,
            UploadedTrackOutputFieldKey.ARTISTS.value,
            UploadedTrackOutputFieldKey.ALBUM.value,
            UploadedTrackOutputFieldKey.TRACK_NUMBER.value,
            UploadedTrackOutputFieldKey.GENRE.value,
            UploadedTrackOutputFieldKey.RATING.value,
            UploadedTrackOutputFieldKey.LANGUAGE.value,
            UploadedTrackOutputFieldKey.PLAYLISTS_PUBLIC.value,
            UploadedTrackOutputFieldKey.PLAY_COUNT.value,
            UploadedTrackOutputFieldKey.ARCHIVED.value,
            UploadedTrackOutputFieldKey.CREATED_ON.value,
            UploadedTrackOutputFieldKey.UPDATED_ON.value,
        ]
