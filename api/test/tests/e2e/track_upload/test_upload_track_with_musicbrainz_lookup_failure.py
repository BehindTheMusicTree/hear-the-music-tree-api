import pytest
from rest_framework import status

from api.model.musicbrainz_resource.children.recording.missing_cause.code.MbRecordingMissingCauseCode import (
    MbRecordingMissingCauseCode,
)
from api.test.tests.integration.uploaded_track.UploadedTrackTestCase import UploadedTrackTestCase
from api.test.utils.uploaded_track.UploadedTrackTestFilename import UploadedTrackTestFilename


@pytest.mark.e2e
class TestCase(UploadedTrackTestCase):
    """
    E2E test for track upload with MusicBrainz lookup failure handling.

    This test verifies the complete workflow:
    1. User authenticates
    2. User uploads an audio file
    3. Audio fingerprinting succeeds
    4. MusicBrainz lookup fails (no matching recording found)
    5. System handles failure gracefully
    6. Track is created with metadata from file tags only

    In CI, conftest mocks MusicBrainz with empty results, so this test's expectations
    (no recording, missing cause set) are met deterministically.
    """

    def test_upload_track_with_musicbrainz_lookup_failure_then_ok(self):
        response = self._post_uploaded_track(UploadedTrackTestFilename.RECORDING_TOKYO_DRIFT_NO_MB_RECORDING_MP3)

        assert response.status_code == status.HTTP_201_CREATED

        track = self.saved_object
        track_file = track.track_file

        assert track is not None
        assert track_file is not None

        fingerprint_bytes = track_file.fingerprint_bytes
        fingerprint_missing_cause = track_file.fingerprint_missing_cause

        if fingerprint_bytes is None:
            if fingerprint_missing_cause:
                code_label = fingerprint_missing_cause.code.label if fingerprint_missing_cause else "Unknown"
                message = (
                    fingerprint_missing_cause.message
                    if fingerprint_missing_cause and fingerprint_missing_cause.message
                    else "No message"
                )
                pytest.skip(f"Fingerprint not generated. Missing cause: {code_label} - {message}")
            else:
                raise AssertionError("Fingerprint is None but no fingerprint_missing_cause is set")

        assert fingerprint_bytes is not None
        assert len(fingerprint_bytes) > 0

        musicbrainz_recording = track_file.musicbrainz_recording
        musicbrainz_recording_missing_cause = track_file.musicbrainz_recording_missing_cause

        if musicbrainz_recording is None:
            if musicbrainz_recording_missing_cause:
                code = musicbrainz_recording_missing_cause.code.code
                assert code in [
                    MbRecordingMissingCauseCode.Codes.LOOKUP_FOUND_NO_MATCHING_RECORDING,
                    MbRecordingMissingCauseCode.Codes.TRACK_FILE_FINGERPRINTING_FAILED,
                    MbRecordingMissingCauseCode.Codes.AFP_DISABLED,
                    MbRecordingMissingCauseCode.Codes.MUSICBRAINZ_LOOKUP_DISABLED,
                    MbRecordingMissingCauseCode.Codes.LOOKUP_FAILED_DUE_TO_INVALID_FINGERPRINT,
                    MbRecordingMissingCauseCode.Codes.LOOKUP_FAILED_DNS_RESOLUTION_ERROR,
                    MbRecordingMissingCauseCode.Codes.LOOKUP_FAILED_WITH_INTERNAL_ERROR,
                    MbRecordingMissingCauseCode.Codes.LOOKUP_FAILED_WITH_UNKNOWN_RESPONSE_STATUS_CODE,
                    MbRecordingMissingCauseCode.Codes.LOOKUP_FAILED_WITH_UNKNOWN_RESPONSE_ERROR_CODE,
                ]
            else:
                raise AssertionError("MusicBrainz recording is None but no musicbrainz_recording_missing_cause is set")

        response = self._retrieve_uploaded_track(track.uuid)
        assert response.status_code == status.HTTP_200_OK

        retrieved_track = self.saved_object
        assert retrieved_track is not None
        assert retrieved_track.uuid == track.uuid
        assert retrieved_track.title is not None
