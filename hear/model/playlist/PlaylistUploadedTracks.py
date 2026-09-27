from typing import TYPE_CHECKING

from django.db import models

if TYPE_CHECKING:
    from the_music_tree_genre_kit.playlist.Playlist import Playlist

    from hear.model.uploaded_track.UploadedTrack import UploadedTrack


def get_uploaded_tracks(playlist: Playlist, archived: bool) -> models.QuerySet[UploadedTrack]:
    """Archiving is hear-only, so the kit Playlist can't filter on it; hear does it here."""
    from hear.model.uploaded_track.UploadedTrack import UploadedTrack

    return UploadedTrack.objects.filter(track_playlist_rels__playlist=playlist, archived=archived)
