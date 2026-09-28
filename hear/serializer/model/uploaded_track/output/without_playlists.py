from rest_framework import serializers
from the_music_tree_api_kit.serializer.EagerLoadingMixin import EagerLoadingMixin

from hear.model.uploaded_track.UploadedTrack import UploadedTrack
from hear.model.uploaded_track.UploadedTrackFieldKey import UploadedTrackFieldKey as ModelFields
from hear.serializer.model.album.minimum import AlbumMinimumSerializer
from hear.serializer.model.artist.minimum import ArtistMinimumSerializer
from hear.serializer.model.criteria.output.minimum import CriteriaMinimumSerializer
from hear.serializer.model.uploaded_track.output.UploadedTrackOutputFieldKey import UploadedTrackOutputFieldKey
from hear.serializer.model.uploaded_track_file.output.detailed import FileDetailedSerializer


class UploadedTrackWithoutPlaylistsSerializer(EagerLoadingMixin, serializers.ModelSerializer):
    file = FileDetailedSerializer(source=ModelFields.TRACK_FILE_INTERNAL.value)
    artists = ArtistMinimumSerializer(many=True)
    album = AlbumMinimumSerializer()
    genre = CriteriaMinimumSerializer()

    @classmethod
    def setup_queryset(cls, queryset, prefix=""):
        track_file = f"{prefix}{ModelFields.TRACK_FILE_INTERNAL.value}"
        return queryset.select_related(
            f"{track_file}__fingerprint_missing_cause__code",
            f"{track_file}__musicbrainz_recording",
            f"{track_file}__musicbrainz_recording_missing_cause__code",
            f"{prefix}album",
            f"{prefix}genre",
        ).prefetch_related(
            f"{prefix}artists",
            f"{prefix}album__album_artists",
            f"{track_file}__musicbrainz_recording__musicbrainz_artists",
        )

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
            UploadedTrackOutputFieldKey.PLAY_COUNT.value,
            UploadedTrackOutputFieldKey.ARCHIVED.value,
            UploadedTrackOutputFieldKey.CREATED_ON.value,
            UploadedTrackOutputFieldKey.UPDATED_ON.value,
        ]
