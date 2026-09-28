from django.db.models import Prefetch
from the_music_tree_genre_kit.playlist.Playlist import Playlist

from hear.serializer.model.playlist.base.output.minimum import PlaylistMinimumSerializer
from hear.serializer.model.uploaded_track.output.UploadedTrackOutputFieldKey import UploadedTrackOutputFieldKey
from hear.serializer.model.uploaded_track.output.without_playlists import UploadedTrackWithoutPlaylistsSerializer


class UploadedTrackDetailedSerializer(UploadedTrackWithoutPlaylistsSerializer):
    playlists = PlaylistMinimumSerializer(many=True)

    @classmethod
    def setup_queryset(cls, queryset, prefix=""):
        return (
            super()
            .setup_queryset(queryset, prefix)
            .prefetch_related(
                Prefetch(
                    f"{prefix}playlists",
                    queryset=PlaylistMinimumSerializer.setup_queryset(Playlist._default_manager.all()),
                )
            )
        )

    class Meta(UploadedTrackWithoutPlaylistsSerializer.Meta):
        fields = [
            *UploadedTrackWithoutPlaylistsSerializer.Meta.fields,
            UploadedTrackOutputFieldKey.PLAYLISTS_PUBLIC.value,
        ]
