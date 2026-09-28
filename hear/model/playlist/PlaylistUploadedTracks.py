from typing import TYPE_CHECKING

from django.db import models
from django.db.models import Count, OuterRef, Subquery, Sum
from django.db.models.functions import Coalesce
from the_music_tree_genre_kit.criteria.track_playlist_rel.Fields import Fields as RelFields
from the_music_tree_genre_kit.criteria.track_playlist_rel.TrackPlaylistRel import TrackPlaylistRel

if TYPE_CHECKING:
    from the_music_tree_genre_kit.playlist.Playlist import Playlist

    from hear.model.uploaded_track.UploadedTrack import UploadedTrack

UPLOADED_TRACKS_COUNT_ANNOTATED = "uploaded_tracks_count_annotated"
UPLOADED_TRACKS_ARCHIVED_COUNT_ANNOTATED = "uploaded_tracks_archived_count_annotated"
DURATION_IN_SEC_ANNOTATED = "duration_in_sec_annotated"


def get_uploaded_tracks(playlist: Playlist, archived: bool) -> models.QuerySet[UploadedTrack]:
    """Archiving is hear-only, so the kit Playlist can't filter on it; hear does it here."""
    from hear.model.uploaded_track.UploadedTrack import UploadedTrack

    return UploadedTrack.objects.filter(track_playlist_rels__playlist=playlist, archived=archived)


def _uploaded_rels(archived: bool) -> models.QuerySet[TrackPlaylistRel]:
    return (
        TrackPlaylistRel._default_manager.filter(
            **{RelFields.PLAYLIST: OuterRef("pk"), f"{RelFields.TRACK_INTERNAL}__uploadedtrack__archived": archived}
        )
        .order_by()
        .values(RelFields.PLAYLIST)
    )


def uploaded_tracks_count_annotation(archived: bool) -> Coalesce:
    """Correlated per-playlist count for `.annotate(...)`, so only the page's rows are counted."""
    return Coalesce(Subquery(_uploaded_rels(archived).annotate(count=Count("pk")).values("count")), 0)


def duration_in_sec_annotation() -> Coalesce:
    """Summed file duration of the playlist's non-archived uploaded tracks."""
    total = _uploaded_rels(archived=False).annotate(
        total=Sum(f"{RelFields.TRACK_INTERNAL}__uploadedtrack__track_file__duration_in_sec")
    )
    return Coalesce(Subquery(total.values("total")), 0)
