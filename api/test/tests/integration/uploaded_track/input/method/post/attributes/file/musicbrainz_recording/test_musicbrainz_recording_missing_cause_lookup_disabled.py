from django.test import override_settings

from rest_framework import status

from api.model.musicbrainz_resource.children.recording.missing_cause.code.MbRecordingMissingCauseCode import (
    MbRecordingMissingCauseCode
)
from api.test.utils.uploaded_track.UploadedTrackTestFilename import UploadedTrackTestFilename
from api.test.tests.integration.uploaded_track.UploadedTrackTestCase import UploadedTrackTestCase


@override_settings(MUSICBRAINZ_LOOKUP_ENABLED=False)
class TestCase(UploadedTrackTestCase):
    def test_afp_enabled_mb_disabled_then_musicbrainz_lookup_disabled_missing_cause(self):
        response = self._post_uploaded_track(UploadedTrackTestFilename.RECORDING_SHOWMUSTGOON_MP3)

        assert response.status_code == status.HTTP_201_CREATED
        assert self.saved_object.track_file.musicbrainz_recording_missing_cause
        assert self.saved_object.track_file.musicbrainz_recording_missing_cause.code.code == \
            MbRecordingMissingCauseCode.Codes.MUSICBRAINZ_LOOKUP_DISABLED
