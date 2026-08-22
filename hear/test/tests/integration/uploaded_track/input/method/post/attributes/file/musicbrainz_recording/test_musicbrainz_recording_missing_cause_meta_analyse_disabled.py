from django.test import override_settings
from rest_framework import status

from hear.model.musicbrainz_resource.children.recording.missing_cause.code.MbRecordingMissingCauseCode import (
    MbRecordingMissingCauseCode,
)
from hear.test.tests.integration.uploaded_track.UploadedTrackTestCase import UploadedTrackTestCase
from hear.test.utils.uploaded_track.UploadedTrackTestFilename import UploadedTrackTestFilename


class TestCase(UploadedTrackTestCase):
    def test_audio_meta_analysis_disabled_then_corresponding_missing_cause(self):
        with override_settings(AFP_ENABLED=False):
            response = self._post_uploaded_track(UploadedTrackTestFilename.RECORDING_SHOWMUSTGOON_MP3)

        assert response.status_code == status.HTTP_201_CREATED
        assert self.saved_object.track_file.musicbrainz_recording_missing_cause
        assert (
            self.saved_object.track_file.musicbrainz_recording_missing_cause.code.code
            == MbRecordingMissingCauseCode.Codes.AFP_DISABLED
        )
