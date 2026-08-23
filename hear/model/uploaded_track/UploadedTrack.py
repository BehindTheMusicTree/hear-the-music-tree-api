from typing import TYPE_CHECKING

from django.db import models
from django.db.models import QuerySet
from the_music_tree_api_kit.field.foreign_key.PrivateOneToOneField import PrivateOneToOneField
from the_music_tree_genre_kit.track.Fields import Fields as TrackFields
from the_music_tree_genre_kit.track.Track import Track

from hear.model.artist.Artist import Artist
from hear.utils.audio_file_metadata.AppMetadataKey import AppMetadataKey

from .file.TrackFile import TrackFile
from .UploadedTrackFieldKey import UploadedTrackFieldKey as Fields
from .UploadedTrackManager import UploadedTrackManager


class UploadedTrack(Track):
    track = PrivateOneToOneField(
        Track, on_delete=models.CASCADE, parent_link=True, related_name=Fields.UPLOADED_TRACK_RELATED_NAME.value
    )
    track_file_fingerprint_must_be_unique = models.BooleanField(default=False)

    if TYPE_CHECKING:
        track_file: TrackFile

    objects: UploadedTrackManager = UploadedTrackManager()

    class Meta:
        db_table = "htmt_api_uploaded_track"
        verbose_name = "Uploaded Track"
        verbose_name_plural = "Uploaded Tracks"

    @property
    def relative_url(self) -> str:
        return f"library/uploaded/{self.uuid}/"

    def __str__(self):
        position_str = f"#{self.track_number}" if self.track_number else "#--"

        artists: QuerySet[Artist] = self.artists.all()
        artists_str = (
            ", ".join(artist.name for artist in artists) if self.artists.exists() else f"[no {TrackFields.ARTISTS}]"
        )
        album_str = str(self.album) if self.album else f"[no {TrackFields.ALBUM}]"

        genre_str = f"{TrackFields.GENRE}: {self.genre}" if self.genre else f"{TrackFields.GENRE}: --"
        rating_str = f"{TrackFields.RATING}: {self.rating}" if self.rating else f"{TrackFields.RATING}: --"
        language_str = f"{TrackFields.LANGUAGE}: {self.language}" if self.language else f"{TrackFields.LANGUAGE}: --"
        file_str = f"{Fields.TRACK_FILE_INTERNAL.value}: {self.track_file}" if self.track_file else "no track file"

        return (
            f"{self.uuid} | {position_str} | '{self.title}' by {artists_str} | {album_str} | "
            f"{genre_str} | {rating_str} | {language_str} | "
            + f"{Fields.CREATED_ON.value}: {self.created_on} | {file_str}"
        )

    def simple_str(self) -> str:
        artists: QuerySet[Artist] = self.artists.all()
        artists_str = ", ".join(artist.name for artist in artists) if self.artists.exists() else f"no {TrackFields.ARTISTS}"
        return f"{self.uuid} | '{self.title}' by {artists_str}"

    def update_file_metadata_from_uploaded_track_instance_values(self):
        """Write current track/album/artist/genre/rating/language into the file. Uses the same metadata keys as
        metadata-session download (APP_METADATA_WRITABLE_KEYS).
        """
        normalized_metadata = {}
        normalized_metadata[AppMetadataKey.TITLE] = self.title

        if self.artists.exists():
            artists_names_tag = [artist.name for artist in self.artists.all()]
        else:
            artists_names_tag = None
        normalized_metadata[AppMetadataKey.ARTISTS_NAMES] = artists_names_tag

        if self.album:
            album_name_tag = self.album.name
            album_artists_list = self.album.album_artists.all()
            album_artists_tag = (
                [album_artist.name for album_artist in album_artists_list] if album_artists_list.exists() else None
            )
        else:
            album_name_tag = None
            album_artists_tag = None

        normalized_metadata[AppMetadataKey.ALBUM_NAME] = album_name_tag
        normalized_metadata[AppMetadataKey.ALBUM_ARTISTS_NAMES] = album_artists_tag
        normalized_metadata[AppMetadataKey.GENRES_NAMES] = [self.genre.name] if self.genre else []
        normalized_metadata[AppMetadataKey.RATING] = self.rating
        normalized_metadata[AppMetadataKey.LANGUAGE] = self.language if self.language else None

        self.track_file.update_file_metadata(app_metadata=normalized_metadata)

    @property
    def playlists_with_positions(self) -> list[tuple[str, int]]:
        from the_music_tree_genre_kit.criteria.track_playlist_rel.Fields import Fields as TrackPlaylistRelFields
        from the_music_tree_genre_kit.criteria.track_playlist_rel.TrackPlaylistRel import TrackPlaylistRel

        track_playlist_rels = TrackPlaylistRel.objects.filter(user=self.user, track=self)
        return list(
            track_playlist_rels.values_list(TrackPlaylistRelFields.PLAYLIST + "__uuid", TrackPlaylistRelFields.POSITION)
        )
