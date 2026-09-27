from typing import TYPE_CHECKING, Any

from django.db import transaction
from django.db.models import QuerySet
from the_music_tree_genre_kit.criteria.track_playlist_rel.TrackPlaylistRel import TrackPlaylistRel
from the_music_tree_genre_kit.track.AbstractTrackManager import AbstractTrackManager

from hear.model.artist.Artist import Artist
from hear.model.uploaded_track.file.Fields import Fields as TrackFileFields

from .UploadedTrackFieldKey import UploadedTrackFieldKey as Fields

if TYPE_CHECKING:
    from .UploadedTrack import UploadedTrack


class UploadedTrackManager(AbstractTrackManager["UploadedTrack"]):
    model: type[UploadedTrack]

    def create(self, **kwargs) -> UploadedTrack:
        from .file.TrackFile import TrackFile

        with transaction.atomic():
            track_file_model_data = {}
            track_file_model_data[TrackFileFields.FILE] = kwargs.pop(Fields.TRACK_FILE_INTERNAL.value)

            instance: UploadedTrack = super().create(**kwargs)

            track_file_model_data[TrackFileFields.USER] = instance.user
            track_file_model_data[TrackFileFields.UPLOADED_TRACK] = instance

            TrackFile.objects.create(**track_file_model_data)

        instance.update_file_metadata_from_uploaded_track_instance_values()
        return instance

    def create_instance_with_track_file(
        self, track_file_data: dict[str, Any], uploaded_track_data: dict[str, Any]
    ) -> UploadedTrack:
        from ..file.TrackFile import TrackFile

        with transaction.atomic():
            artists = uploaded_track_data.pop(Fields.ARTISTS.value, None)
            uploaded_track: UploadedTrack = self.model(**uploaded_track_data)
            uploaded_track.save()
            if artists:
                uploaded_track.artists.set(artists)

            track_file_data[TrackFileFields.UPLOADED_TRACK] = uploaded_track
            TrackFile.objects.create(**track_file_data)

        uploaded_track.update_file_metadata_from_uploaded_track_instance_values()

        return uploaded_track

    def update_instance(self, old_instance: UploadedTrack, **kwargs) -> UploadedTrack:
        was_archived = old_instance.archived
        with transaction.atomic():
            updated_instance: UploadedTrack = super().update_instance(old_instance, **kwargs)
            if was_archived != updated_instance.archived:
                if updated_instance.archived:
                    self._archive_playlist_rels(updated_instance)
                else:
                    self._unarchive_playlist_rels(updated_instance)
            updated_instance.update_file_metadata_from_uploaded_track_instance_values()
            return updated_instance

    @staticmethod
    def _archive_playlist_rels(uploaded_track: UploadedTrack) -> None:
        """An archived track keeps its playlist rels with a null position."""
        for rel in TrackPlaylistRel.objects.filter(track=uploaded_track, position__isnull=False):
            old_position = rel.position
            rel.position = None
            rel.save(update_fields=["position"])
            TrackPlaylistRel.objects._decrement_positions_of_following_tracks(rel.playlist, old_position)

    @staticmethod
    def _unarchive_playlist_rels(uploaded_track: UploadedTrack) -> None:
        for rel in TrackPlaylistRel.objects.filter(track=uploaded_track, position__isnull=True):
            TrackPlaylistRel.objects._increment_positions_of_following_tracks(rel.playlist, 1)
            rel.position = 1
            rel.save(update_fields=["position"])

    def delete_with_checking_artists_potential_deletion(self, instance: UploadedTrack):
        track_artists: QuerySet[Artist] = instance.artists.all()
        instance.delete()
        for artist in track_artists:
            Artist.objects.delete_instance_if_nothing_linked(artist)
