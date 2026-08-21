from django.db import models
from the_music_tree_api_kit.field.foreign_key.PrivateOneToOneField import PrivateOneToOneField
from the_music_tree_genre_kit.criteria.playlist.AbstractCriteriaPlaylist import AbstractCriteriaPlaylist

from api.model.playlist.Fields import Fields as PlayListFields
from api.model.playlist.Playlist import Playlist

from .CriteriaPlaylistManager import CriteriaPlaylistManager
from .Fields import Fields


# django-stubs can't resolve the track_playlist_rels reverse manager for a
# settings.PLAYLIST_MODEL-targeted FK declared in the kit on an MTI child; Django
# resolves it fine at runtime (tests + makemigrations --check pass clean).
class CriteriaPlaylist(AbstractCriteriaPlaylist, Playlist):  # type: ignore[django-manager-missing]
    playlist = PrivateOneToOneField(
        Playlist, on_delete=models.CASCADE, parent_link=True, related_name=PlayListFields.CRITERIA_PLAYLIST
    )

    objects: CriteriaPlaylistManager = CriteriaPlaylistManager()

    class Meta:
        db_table = "htmt_api_criteria_playlist"
        verbose_name = "Criteria Playlist"
        verbose_name_plural = "Criteria Playlists"
        indexes = [
            models.Index(fields=[Fields.CRITERIA], name="crit_playlist_criteria_idx"),
        ]
