import pytest
from rest_framework import status

from api.model.musicbrainz_resource.children.recording.missing_cause.code.MbRecordingMissingCauseCode import (
    MbRecordingMissingCauseCode
)
from api.test.utils.uploaded_track.UploadedTrackTestFilename import UploadedTrackTestFilename
from api.test.tests.integration.uploaded_track.UploadedTrackTestCase import UploadedTrackTestCase


@pytest.mark.parametrize('enable_audio_metadata_analysis', [False], indirect=True)
class TestCase(UploadedTrackTestCase):
    def test_audio_meta_analysis_disabled_then_corresponding_missing_cause(self, enable_audio_metadata_analysis):
        response = self._post_uploaded_track(UploadedTrackTestFilename.RECORDING_SHOWMUSTGOON_MP3)

        assert response.status_code == status.HTTP_201_CREATED
        assert self.saved_object.track_file.musicbrainz_recording_missing_cause
        assert self.saved_object.track_file.musicbrainz_recording_missing_cause.code.code == \
            MbRecordingMissingCauseCode.Codes.AUDIO_META_AMALYSIS_DISABLED
