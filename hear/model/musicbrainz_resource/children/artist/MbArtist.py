from django.db import models
from django.db.models import F, Value
from the_music_tree_api_kit.field.AppCharField import AppCharField

from hear import settings
from hear.model.utils.ConcatOp import ConcatOp

from ...MusicbrainzResource import MusicbrainzResource
from .Fields import Fields


class MbArtist(MusicbrainzResource):
    musicbrainz_link = models.GeneratedField(  # type: ignore
        expression=ConcatOp(Value(settings.MB_ARTIST_URL), F(Fields.MUSICBRAINZ_ID)),
        output_field=AppCharField(max_length=len(settings.MB_RECORDING_URL) + settings.UUID_LEN),
        db_persist=True,
    )
    name = AppCharField(max_length=settings.MB_ARTIST_NAME_LEN_MAX, default=None)

    def __str__(self):
        return f"{self.musicbrainz_id} | {self.name}"

    class Meta:
        db_table = "htmt_api_mb_artist"
        verbose_name = "Musicbrainz Artist"
        verbose_name_plural = "Musicbrainz Artists"
        indexes = [models.Index(fields=[Fields.MUSICBRAINZ_ID], name="mb_artist_id_idx")]
