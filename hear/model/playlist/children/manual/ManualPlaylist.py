from django.db import models
from the_music_tree_api_kit.field.foreign_key.PrivateOneToOneField import PrivateOneToOneField
from the_music_tree_genre_kit.manual_playlist.AbstractManualPlaylist import AbstractManualPlaylist
from the_music_tree_genre_kit.playlist.Fields import Fields as PlayListFields
from the_music_tree_genre_kit.playlist.Playlist import Playlist as KitPlaylist

from hear.model.uploaded_track_mixin.UploadedTrackMixinWithInternalNameManager import (
    UploadedTrackMixinWithInternalNameManager,
)

from .Fields import Fields


class ManualPlaylist(AbstractManualPlaylist, KitPlaylist):  # type: ignore[django-manager-missing]
    playlist = PrivateOneToOneField(
        KitPlaylist, on_delete=models.CASCADE, parent_link=True, related_name=PlayListFields.MANUAL_PLAYLIST
    )

    objects: UploadedTrackMixinWithInternalNameManager = UploadedTrackMixinWithInternalNameManager()

    class Meta:
        db_table = "htmt_api_manual_playlist"
        constraints = [models.CheckConstraint(condition=~models.Q(_name=""), name="manual_playlist_non_empty_name")]
        verbose_name = "Manual Playlist"
        verbose_name_plural = "Manual Playlists"
        indexes = [models.Index(fields=[Fields.NAME_INTERNAL], name="manual_playlist_name_idx")]
