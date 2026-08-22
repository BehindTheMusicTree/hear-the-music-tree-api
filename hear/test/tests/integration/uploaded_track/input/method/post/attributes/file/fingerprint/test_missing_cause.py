from unittest.mock import patch

import pytest
from rest_framework import status

from hear.model.uploaded_track.file.fingerprinting.missing_cause.code.FingerprintMissingCauseCode import (
    FingerprintMissingCauseCode,
)
from hear.test.tests.integration.uploaded_track.UploadedTrackTestCase import UploadedTrackTestCase
from hear.test.utils.uploaded_track.UploadedTrackTestFilename import UploadedTrackTestFilename
from hear.utils.audio_fingerprinter import exception as audio_fingerprinter_exc


class TestCase(UploadedTrackTestCase):
    @patch("hear.utils.audio_fingerprinter.utils.post_fingerprint_audio")
    def test_audio_fingerprinter_service_down_then_corresponding_missing_cause(self, mock_post_fingerprint):
        mock_post_fingerprint.side_effect = audio_fingerprinter_exc.ServiceNotFoundException(
            "Connection refused (service down)"
        )
        response = self._post_uploaded_track(UploadedTrackTestFilename.RECORDING_SHOWMUSTGOON_MP3)

        assert response.status_code == status.HTTP_201_CREATED
        assert self.saved_object.track_file and self.saved_object.track_file.fingerprint_missing_cause
        assert self.saved_object.track_file.fingerprint_missing_cause.code.code in [
            FingerprintMissingCauseCode.Codes.SERVICE_NOT_FOUND,
            FingerprintMissingCauseCode.Codes.UNKNOWN_CONNEXION_ERROR,
        ]

    def test_audio_fingerprinter_service_ok_then_no_missing_cause(self):
        response = self._post_uploaded_track(UploadedTrackTestFilename.RECORDING_SHOWMUSTGOON_MP3)

        assert response.status_code == status.HTTP_201_CREATED
        assert not self.saved_object.track_file.fingerprint_missing_cause
