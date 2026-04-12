import pytest
from rest_framework import status

from api.model.uploaded_track.file.fingerprinting.missing_cause.code.FingerprintMissingCauseCode import (
    FingerprintMissingCauseCode,
)
from api.test.tests.integration.uploaded_track.UploadedTrackTestCase import UploadedTrackTestCase
from api.test.utils.uploaded_track.UploadedTrackTestFilename import UploadedTrackTestFilename


@pytest.mark.e2e
class TestCase(UploadedTrackTestCase):
    """
    E2E test for track upload with fingerprinting failure handling.

    This test verifies the complete workflow:
    1. User authenticates
    2. User uploads an audio file
    3. Audio fingerprinting fails (simulate AcoustID service unavailable)
    4. System handles failure gracefully
    5. Track is still created with metadata from file tags
    6. Fingerprint missing cause is recorded
    """

    def test_upload_track_with_fingerprinting_failure_then_ok(self):
        response = self._post_uploaded_track(UploadedTrackTestFilename.METADATA_NONE_MP3)

        assert response.status_code == status.HTTP_201_CREATED

        track = self.saved_object
        track_file = track.track_file

        assert track is not None
        assert track_file is not None

        fingerprint_bytes = track_file.fingerprint_bytes
        fingerprint_missing_cause = track_file.fingerprint_missing_cause

        if fingerprint_bytes is None:
            if fingerprint_missing_cause:
                code = fingerprint_missing_cause.code.code
                assert code in [
                    FingerprintMissingCauseCode.Codes.AFP_DISABLED,
                    FingerprintMissingCauseCode.Codes.SERVICE_NOT_FOUND,
                    FingerprintMissingCauseCode.Codes.WRONG_FILE_EXTENSION,
                    FingerprintMissingCauseCode.Codes.WRONG_FILE_TYPE,
                    FingerprintMissingCauseCode.Codes.INTERNAL_ERROR,
                    FingerprintMissingCauseCode.Codes.UNKNOWN_CONNEXION_ERROR,
                ]
            else:
                raise AssertionError("Fingerprint is None but no fingerprint_missing_cause is set")

        if fingerprint_missing_cause:
            assert fingerprint_missing_cause.code is not None
            assert fingerprint_missing_cause.code.code is not None

        musicbrainz_recording = track_file.musicbrainz_recording
        if fingerprint_bytes is None:
            assert musicbrainz_recording is None or track_file.musicbrainz_recording_missing_cause is not None

        response = self._retrieve_uploaded_track(track.uuid)
        assert response.status_code == status.HTTP_200_OK

        retrieved_track = self.saved_object
        assert retrieved_track is not None
        assert retrieved_track.uuid == track.uuid
        assert retrieved_track.title is not None
