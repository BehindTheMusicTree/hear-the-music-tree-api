from django.db import models
from the_music_tree_api_kit.field.AppCharField import AppCharField
from the_music_tree_api_kit.field.foreign_key.PrivateOneToOneField import PrivateOneToOneField

from api import settings
from api.model.playlist.children.manual import ManualPlaylistTypeLabel
from api.model.playlist.Fields import Fields as PlayListFields
from api.model.playlist.Playlist import Playlist
from api.model.uploaded_track_mixin.UploadedTrackMixinWithInternalNameManager import (
    UploadedTrackMixinWithInternalNameManager,
)

from .Fields import Fields


class ManualPlaylist(Playlist):
    playlist = PrivateOneToOneField(
        Playlist, on_delete=models.CASCADE, parent_link=True, related_name=PlayListFields.MANUAL_PLAYLIST
    )

    _name = AppCharField(
        max_length=settings.MANUAL_PLAYLIST_NAME_LEN_MAX, blank=False, null=False, db_column=Fields.NAME_PUBLIC
    )  # type: ignore

    objects: UploadedTrackMixinWithInternalNameManager = UploadedTrackMixinWithInternalNameManager()

    @property
    def name(self) -> str:
        return self._name

    class Meta:
        db_table = "htmt_api_manual_playlist"
        constraints = [models.CheckConstraint(condition=~models.Q(_name=""), name="manual_playlist_non_empty_name")]
        verbose_name = "Manual Playlist"
        verbose_name_plural = "Manual Playlists"
        indexes = [models.Index(fields=[Fields.NAME_INTERNAL], name="manual_playlist_name_idx")]

    @property
    def type_label(self):
        return ManualPlaylistTypeLabel.VALUE
