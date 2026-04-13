from django.core.files.base import File as DjangoFile

from api.model.uploaded_track.file.fingerprinting.FingerprintingResult import FingerprintingResult
from api.model.uploaded_track.file.fingerprinting.missing_cause.code.FingerprintMissingCauseCode import (
    FingerprintMissingCauseCode,
)
from api.model.uploaded_track.file.fingerprinting.missing_cause.FingerprintMissingCause import FingerprintMissingCause
from api.model.user.User import User

from . import utils
from .utils import exception as audio_fingerprinter_exc

USER_ID_PLACEHOLDER_FOR_ANALYSIS = "anonymous"

RESULT_FINGERPRINT = "fingerprint"
RESULT_DURATION_IN_SEC = "duration_in_sec"
RESULT_ERROR_CODE = "error_code"
RESULT_ERROR_MESSAGE = "error_message"

_EPHEMERAL_ERROR_MAPPING = {
    audio_fingerprinter_exc.WrongFileExtension: "wrong_file_extension",
    audio_fingerprinter_exc.WrongFileType: "wrong_file_type",
    audio_fingerprinter_exc.FileNotInPool: "file_not_in_pool",
    audio_fingerprinter_exc.BadRequestException: "unknown_bad_request",
    audio_fingerprinter_exc.InternalServerException: "internal_error",
    audio_fingerprinter_exc.TimeoutException: "timeout_error",
    audio_fingerprinter_exc.FpcalcStatusException: "fpcalc_error_with_status_2",
    audio_fingerprinter_exc.UnknownUnprocessableEntityException: "unknown_unprocessable_entity_error",
    audio_fingerprinter_exc.ServiceNotFoundException: "service_not_found",
    audio_fingerprinter_exc.ConnectionException: "unknown_connexion_error",
}


def _get_fingerprint_and_duration_from_file(user_id: str, file, title: str) -> tuple[bytes, int]:
    from api.utils.file_path_utils import get_file_name_system

    filename = get_file_name_system(file)
    fingerprint, duration_in_sec = utils.post_fingerprint_audio(filename=filename, title=title, user_id=user_id)
    return fingerprint, int(duration_in_sec)


def get_fingerprinting_result(user: User, track_file: DjangoFile, title: str) -> FingerprintingResult:

    duration_in_sec = None
    fingerprint = None
    fingerprint_missing_cause = None
    try:
        fingerprint, duration_in_sec = _get_fingerprint_and_duration_from_file(
            user_id=user.pk, file=track_file, title=title
        )

    except audio_fingerprinter_exc.AudioFingerprinterException as e:
        fingerprint = None
        error_mapping = {
            audio_fingerprinter_exc.WrongFileExtension: FingerprintMissingCauseCode.Codes.WRONG_FILE_EXTENSION,
            audio_fingerprinter_exc.WrongFileType: FingerprintMissingCauseCode.Codes.WRONG_FILE_TYPE,
            audio_fingerprinter_exc.FileNotInPool: FingerprintMissingCauseCode.Codes.FILE_NOT_FOUND_IN_POOL,
            audio_fingerprinter_exc.BadRequestException: FingerprintMissingCauseCode.Codes.UNKNOWN_BAD_REQUEST,
            audio_fingerprinter_exc.InternalServerException: FingerprintMissingCauseCode.Codes.INTERNAL_ERROR,
            audio_fingerprinter_exc.TimeoutException: FingerprintMissingCauseCode.Codes.TIMEOUT_ERROR,
            audio_fingerprinter_exc.FpcalcStatusException: FingerprintMissingCauseCode.Codes.FPCALC_ERROR_WITH_STATUS_2,
            audio_fingerprinter_exc.UnknownUnprocessableEntityException: FingerprintMissingCauseCode.Codes.UNKNOWN_UNPROCESSABLE_ENTITY_ERROR,
            audio_fingerprinter_exc.ServiceNotFoundException: FingerprintMissingCauseCode.Codes.SERVICE_NOT_FOUND,
            audio_fingerprinter_exc.ConnectionException: FingerprintMissingCauseCode.Codes.UNKNOWN_CONNEXION_ERROR,
        }

        fingerprinting_missing_cause_code = error_mapping.get(e.__class__)

        fingerprint_missing_cause = FingerprintMissingCause.objects.create(
            user=user, code=fingerprinting_missing_cause_code, message=e.message
        )

    return FingerprintingResult(
        fingerprint=fingerprint, duration_in_sec=duration_in_sec, error=fingerprint_missing_cause
    )


def get_fingerprint_and_duration_for_analysis(file, title: str = "") -> dict:
    """Return fingerprint and duration for analysis without persisting or requiring a user."""
    from api.utils.file_path_utils import get_file_name_system

    filename = get_file_name_system(file)
    try:
        fingerprint, duration_in_sec = utils.post_fingerprint_audio(
            filename=filename, title=title, user_id=USER_ID_PLACEHOLDER_FOR_ANALYSIS
        )
        return {
            RESULT_FINGERPRINT: fingerprint,
            RESULT_DURATION_IN_SEC: float(duration_in_sec),
            RESULT_ERROR_CODE: None,
            RESULT_ERROR_MESSAGE: None,
        }
    except audio_fingerprinter_exc.AudioFingerprinterException as e:
        error_code = _EPHEMERAL_ERROR_MAPPING.get(type(e), "unknown")
        message = getattr(e, "message", str(e))
        return {
            RESULT_FINGERPRINT: None,
            RESULT_DURATION_IN_SEC: None,
            RESULT_ERROR_CODE: error_code,
            RESULT_ERROR_MESSAGE: message,
        }
