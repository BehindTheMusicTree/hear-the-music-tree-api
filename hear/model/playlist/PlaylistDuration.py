from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from the_music_tree_genre_kit.playlist.Playlist import Playlist


def get_duration_in_sec(playlist: Playlist) -> int:
    """Genre-kit's Playlist/TrackMixin has no notion of file duration (it's generic across
    apps), so hear computes it here from its own UploadedTrack/TrackFile.
    """
    from hear.model.uploaded_track.UploadedTrack import UploadedTrack

    uploaded_tracks = UploadedTrack.objects.filter(track_playlist_rels__playlist=playlist, archived=False)
    return sum(
        int(uploaded_track.track_file.duration_in_sec or 0) if uploaded_track.track_file else 0
        for uploaded_track in uploaded_tracks
    )


def get_duration_str_in_hour_min_sec(playlist: Playlist) -> str:
    total_seconds = get_duration_in_sec(playlist)
    hours = total_seconds // 3600
    minutes = (total_seconds % 3600) // 60
    seconds = total_seconds % 60
    return f"{hours:02}:{minutes:02}:{seconds:02}"
