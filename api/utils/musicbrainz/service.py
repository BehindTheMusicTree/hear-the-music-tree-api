

import acoustid
from acoustid import WebServiceError
from django.core.exceptions import ObjectDoesNotExist

from api import settings
from api.exception import musicbrainz as musicbrainz_exception
from api.model.musicbrainz_resource.children.recording.MbRecording import MbRecording
from api.model.musicbrainz_resource.children.recording.MbRecordingLookupResult import (
    MusicbrainzRecordingLookupResult
)
from api.model.musicbrainz_resource.children.recording.missing_cause.code.MbRecordingMissingCauseCode import (
    MbRecordingMissingCauseCode
)
from api.model.musicbrainz_resource.children.recording.missing_cause.MbRecordingMissingCause import (
    MbRecordingMissingCause
)
from api.model.user.User import User

from . import utils
from .ApiFields import ApiFields
from .LookupMetaFields import LookupMetaFields


def _get_musicbrainz_best_recording_dict_from_fingerprint_and_duration(fingerprint: bytes,
                                                                       duration_in_sec: float) -> dict | None:
    try:
        lookup = acoustid.lookup(apikey=settings.ACOUSTID_API_KEY,
                                 fingerprint=fingerprint,
                                 duration=duration_in_sec,
                                 meta=[LookupMetaFields.RECORDINGS,
                                       LookupMetaFields.RELEASE_GROUPS,
                                       LookupMetaFields.RELEASES,
                                       LookupMetaFields.COMPRESS,
                                       LookupMetaFields.TRACKS])

        lookup_status = lookup[ApiFields.Names.STATUS]
        if lookup_status == ApiFields.Values.Status.OK:
            recordings_grouped_by_score = lookup[ApiFields.Names.RESULTS]
            if len(recordings_grouped_by_score) > 0:
                return utils.get_best_recording_dict_with_score(recordings_grouped_by_score=recordings_grouped_by_score,
                                                                duration_in_sec=duration_in_sec)
            else:
                return None
        elif lookup_status == ApiFields.Values.Status.ERROR:
            error_dict = lookup[ApiFields.Names.ERROR]
            error_code = error_dict[ApiFields.Names.CODE]
            error_message = error_dict[ApiFields.Names.MESSAGE]
            if error_code == 3:
                raise musicbrainz_exception.InvalidFingerprintMusicbrainzRecordingLookupException(
                    f"Musicbrainz original lookup error message: \"{error_message}\"")
            elif error_code == 5:
                raise musicbrainz_exception.InternalErrorMusicbrainzRecordingLookupException(
                    f"Musicbrainz original lookup error message: \"{error_message}\"")
            else:
                exception_message = f"Error while getting MusicBrainz recording ID: {error_code} - {error_message}"
                raise musicbrainz_exception.UnknownErrorCodeMusicbrainzRecordingLookupException(exception_message)
        else:
            raise musicbrainz_exception.UnknownStatusMusicbrainzRecordingLookupException(lookup_status)
    except Exception as exception:
        if isinstance(exception, musicbrainz_exception.MusicbrainzRecordingLookupException):
            raise exception
        if isinstance(exception, WebServiceError):
            try:
                exc_str = str(exception)
            except Exception:
                exc_str = f"{type(exception).__name__}: <unable to stringify exception>"
            raise musicbrainz_exception.DNSResolutionErrorMusicbrainzRecordingLookupException(exc_str)
        try:
            exc_str = str(exception)
        except Exception:
            exc_str = f"{type(exception).__name__}: <unable to stringify exception>"
        raise musicbrainz_exception.UnknownErrorCodeMusicbrainzRecordingLookupException(exc_str)


def get_musicbrainz_recording_lookup_result(user: User,
                                            fingerprint: bytes,
                                            duration_in_sec: float) -> MusicbrainzRecordingLookupResult:
    musicbrainz_recording = None
    musicbrainz_recording_missing_cause = None
    musicbrainz_recording_missing_cause_code = None
    musicbrainz_recording_missing_cause_message = None

    if duration_in_sec <= 1:
        musicbrainz_recording_missing_cause_code = MbRecordingMissingCauseCode.Codes.DURATION_BELOW_OR_EQUAL_1_SEC
    elif not (getattr(settings, 'ACOUSTID_API_KEY', None) or '').strip():
        musicbrainz_recording_missing_cause_code = MbRecordingMissingCauseCode.Codes.LOOKUP_FOUND_NO_MATCHING_RECORDING
    else:
        try:
            musicbrainz_recording_dict = _get_musicbrainz_best_recording_dict_from_fingerprint_and_duration(
                fingerprint=fingerprint, duration_in_sec=duration_in_sec)
            if not musicbrainz_recording_dict:
                musicbrainz_recording_missing_cause_code = \
                    MbRecordingMissingCauseCode.Codes.LOOKUP_FOUND_NO_MATCHING_RECORDING
                musicbrainz_recording_missing_cause_message = None
            else:
                musicbrainz_recording_id = musicbrainz_recording_dict[ApiFields.Names.ID]
                musicbrainz_recording = utils.create_or_update_musicbrainz_recording_instance_from_dict(
                    musicbrainz_recording_id=musicbrainz_recording_id,
                    musicbrainz_recording_dict=musicbrainz_recording_dict)

        except musicbrainz_exception.MusicbrainzRecordingLookupException as e:
            exception_mapping: dict[type, MbRecordingMissingCauseCode.Codes] = {
                musicbrainz_exception.InvalidFingerprintMusicbrainzRecordingLookupException:
                    MbRecordingMissingCauseCode.Codes.LOOKUP_FAILED_DUE_TO_INVALID_FINGERPRINT,
                musicbrainz_exception.InternalErrorMusicbrainzRecordingLookupException:
                    MbRecordingMissingCauseCode.Codes.LOOKUP_FAILED_WITH_INTERNAL_ERROR,
                musicbrainz_exception.UnknownErrorCodeMusicbrainzRecordingLookupException:
                    MbRecordingMissingCauseCode.Codes.LOOKUP_FAILED_WITH_UNKNOWN_RESPONSE_ERROR_CODE,
                musicbrainz_exception.UnknownStatusMusicbrainzRecordingLookupException:
                    MbRecordingMissingCauseCode.Codes.LOOKUP_FAILED_WITH_UNKNOWN_RESPONSE_STATUS_CODE,
                musicbrainz_exception.DNSResolutionErrorMusicbrainzRecordingLookupException:
                    MbRecordingMissingCauseCode.Codes.LOOKUP_FAILED_DNS_RESOLUTION_ERROR}
            musicbrainz_recording_missing_cause_code = exception_mapping[type(e)]
            error_message = str(e)
            if len(error_message) > settings.MB_RECORDING_MISSING_CAUSE_MESSAGE_LEN_MAX:
                musicbrainz_recording_missing_cause_message = error_message[
                    :settings.MB_RECORDING_MISSING_CAUSE_MESSAGE_LEN_MAX - 3] + "..."
            else:
                musicbrainz_recording_missing_cause_message = error_message

    if musicbrainz_recording_missing_cause_code:
        musicbrainz_recording_missing_cause = MbRecordingMissingCause.objects.create(
            user=user,
            code=musicbrainz_recording_missing_cause_code,
            message=musicbrainz_recording_missing_cause_message)

    return MusicbrainzRecordingLookupResult(recording=musicbrainz_recording,
                                            missing_cause=musicbrainz_recording_missing_cause)


ANALYSIS_ERROR = "error"
ANALYSIS_CODE = "code"
ANALYSIS_MESSAGE = "message"

ERROR_DURATION_TOO_SHORT = "duration_below_or_equal_1_sec"
ERROR_NO_API_KEY = "no_acoustid_api_key"
ERROR_NO_MATCH = "no_match"
ERROR_INVALID_FINGERPRINT = "invalid_fingerprint"
ERROR_INTERNAL = "internal_error"
ERROR_UNKNOWN_RESPONSE_CODE = "unknown_response_error_code"
ERROR_UNKNOWN_STATUS = "unknown_response_status_code"
ERROR_DNS = "dns_resolution_error"
ERROR_UNKNOWN = "unknown_error"

_EXCEPTION_TO_ERROR_CODE = {
    musicbrainz_exception.InvalidFingerprintMusicbrainzRecordingLookupException: ERROR_INVALID_FINGERPRINT,
    musicbrainz_exception.InternalErrorMusicbrainzRecordingLookupException: ERROR_INTERNAL,
    musicbrainz_exception.UnknownErrorCodeMusicbrainzRecordingLookupException: ERROR_UNKNOWN_RESPONSE_CODE,
    musicbrainz_exception.UnknownStatusMusicbrainzRecordingLookupException: ERROR_UNKNOWN_STATUS,
    musicbrainz_exception.DNSResolutionErrorMusicbrainzRecordingLookupException: ERROR_DNS,
}


def get_musicbrainz_recording_analysis(fingerprint: bytes, duration_in_sec: float) -> dict:
    """Return raw AcoustID/MusicBrainz recording dict or error dict; no DB writes."""
    if duration_in_sec <= 1:
        return {
            ANALYSIS_ERROR: ERROR_DURATION_TOO_SHORT,
            ANALYSIS_CODE: ERROR_DURATION_TOO_SHORT,
            ANALYSIS_MESSAGE: "Duration must be greater than 1 second for AcoustID lookup.",
        }
    if not (getattr(settings, "ACOUSTID_API_KEY", None) or "").strip():
        return {
            ANALYSIS_ERROR: ERROR_NO_API_KEY,
            ANALYSIS_CODE: ERROR_NO_API_KEY,
            ANALYSIS_MESSAGE: "AcoustID API key not configured.",
        }
    try:
        recording_dict = _get_musicbrainz_best_recording_dict_from_fingerprint_and_duration(
            fingerprint=fingerprint, duration_in_sec=duration_in_sec
        )
        if not recording_dict:
            return {
                ANALYSIS_ERROR: ERROR_NO_MATCH,
                ANALYSIS_CODE: ERROR_NO_MATCH,
                ANALYSIS_MESSAGE: "No matching recording found.",
            }
        return recording_dict
    except musicbrainz_exception.MusicbrainzRecordingLookupException as e:
        code = _EXCEPTION_TO_ERROR_CODE.get(type(e), ERROR_UNKNOWN)
        return {
            ANALYSIS_ERROR: code,
            ANALYSIS_CODE: code,
            ANALYSIS_MESSAGE: str(e),
        }
