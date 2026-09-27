from the_music_tree_genre_kit.playlist.Playlist import Playlist

from hear.model.playlist.PlaylistUploadedTracks import get_uploaded_tracks


class UploadedTracksCountsMixin:
    def get_uploaded_tracks_count(self, obj: Playlist) -> int:
        return get_uploaded_tracks(obj, archived=False).count()

    def get_uploaded_tracks_archived_count(self, obj: Playlist) -> int:
        return get_uploaded_tracks(obj, archived=True).count()
