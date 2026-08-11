from django.db import models
from the_music_tree_api_kit.private_unique_resource.PrivateUniqueResource import PrivateUniqueResource

from api import settings
from api.model.field.AppCharField import AppCharField
from api.model.field.foreign_key.AppForeignKey import AppForeignKey

from .code.FingerprintMissingCauseCode import FingerprintMissingCauseCode
from .FingerprintMissingCauseManager import FingerprintMissingCauseManager


class FingerprintMissingCause(PrivateUniqueResource):
    code: FingerprintMissingCauseCode = AppForeignKey(  # type: ignore
        FingerprintMissingCauseCode, on_delete=models.DO_NOTHING
    )
    message = AppCharField(max_length=settings.FINGERPRINTING_ERROR_MESSAGE_LEN_MAX, null=True)

    objects = FingerprintMissingCauseManager()

    def __str__(self) -> str:
        return f"{self.code} | {self.message}"

    class Meta:
        db_table = "htmt_api_fingerprint_missing_cause"
        verbose_name = "Fingerprinting Error"
        verbose_name_plural = "Fingerprinting Errors"
