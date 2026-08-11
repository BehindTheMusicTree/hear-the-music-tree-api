from django.db import models
from the_music_tree_api_kit.field.AppCharField import AppCharField
from the_music_tree_api_kit.field.foreign_key.AppForeignKey import AppForeignKey
from the_music_tree_api_kit.private_standard_resource.PrivateStandardResource import PrivateStandardResource

from api import settings

from .code.MbRecordingMissingCauseCode import MbRecordingMissingCauseCode
from .MbRecordingMissingCauseManager import MbRecordingMissingCauseManager


class MbRecordingMissingCause(PrivateStandardResource):
    code: MbRecordingMissingCauseCode = AppForeignKey(  # type: ignore
        MbRecordingMissingCauseCode, on_delete=models.DO_NOTHING
    )
    message = AppCharField(max_length=settings.MB_RECORDING_MISSING_CAUSE_MESSAGE_LEN_MAX, null=True)

    objects: MbRecordingMissingCauseManager = MbRecordingMissingCauseManager()

    class Meta:
        db_table = "htmt_api_mb_recording_missing_cause"
        verbose_name = "MusicBrainz Recording Missing Cause"
        verbose_name_plural = "MusicBrainz Recording Missing Causes"

    def __str__(self):
        return f"{self.user}: {self.code} - {self.message}"
