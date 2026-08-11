from django.contrib.auth import get_user_model
from django.db import models
from django.db.models import Case, F, Value, When
from the_music_tree_api_kit.field.foreign_key.PrivateForeignKey import PrivateForeignKey
from the_music_tree_api_kit.private_standard_resource.PrivateStandardResource import PrivateStandardResource

from api.model.playlist.Fields import Fields as PlayListFields
from api.model.playlist.Playlist import Playlist
from api.model.uploaded_track.UploadedTrack import UploadedTrack
from api.model.uploaded_track.UploadedTrackFieldKey import UploadedTrackFieldKey as UploadedTrackFields
from api.model.uploaded_track_playlist_rel.UploadedTrackPlaylistRelManager import UploadedTrackPlaylistRelManager

from .Fields import Fields

User = get_user_model()


class UploadedTrackPlaylistRel(PrivateStandardResource):
    playlist: Playlist = PrivateForeignKey(  # type: ignore
        Playlist, on_delete=models.CASCADE, related_name=PlayListFields.UPLOADED_TRACK_PLAYLIST_RELS_INTERNAL
    )
    uploaded_track: UploadedTrack = PrivateForeignKey(  # type: ignore
        UploadedTrack, on_delete=models.CASCADE, related_name=UploadedTrackFields.UPLOADED_TRACK_PLAYLIST_RELS.value
    )
    position = models.PositiveIntegerField(null=True, blank=True)

    objects: UploadedTrackPlaylistRelManager = UploadedTrackPlaylistRelManager()

    class Meta:
        db_table = "htmt_api_uploaded_track_playlist_rel"
        verbose_name = "Uploaded Track Playlist Relation"
        verbose_name_plural = "Uploaded Track Playlist Relations"
        indexes = [
            models.Index(fields=[Fields.USER, Fields.PLAYLIST]),
            models.Index(fields=[Fields.USER, Fields.UPLOADED_TRACK_INTERNAL]),
        ]

    def __str__(self):
        return (
            f'Playlist "{self.playlist.name}" | Lib track title "{self.uploaded_track.title}" | '
            f"Position {self.position} User {self.user}"
        )

    def _perform_save(self, adding: bool, ctx) -> None:
        if adding:
            uploaded_track_playlist_rels = UploadedTrackPlaylistRel.objects.filter(
                user=self.user, playlist=self.playlist
            )
            uploaded_track_playlist_rels.update(
                position=Case(
                    When(**{Fields.POSITION + "__isnull": False}, then=F(Fields.POSITION) + 1), default=Value(None)
                )
            )
            self.position = 1
        super()._perform_save(adding, ctx)
