from django.db import models
from the_music_tree_genre_kit.criteria.track_playlist_rel.AbstractTrackPlaylistRel import AbstractTrackPlaylistRel

from .Fields import Fields
from .TrackPlaylistRelManager import TrackPlaylistRelManager


class TrackPlaylistRel(AbstractTrackPlaylistRel):
    objects: TrackPlaylistRelManager = TrackPlaylistRelManager()

    class Meta:
        db_table = "htmt_api_uploaded_track_playlist_rel"
        verbose_name = "Track Playlist Relation"
        verbose_name_plural = "Track Playlist Relations"
        indexes = [
            models.Index(fields=[Fields.USER, Fields.PLAYLIST]),
            models.Index(fields=[Fields.USER, Fields.TRACK_INTERNAL]),
        ]
