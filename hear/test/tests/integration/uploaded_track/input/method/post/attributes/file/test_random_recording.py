from rest_framework import status

from hear.test.tests.integration.uploaded_track.UploadedTrackTestCase import UploadedTrackTestCase
from hear.test.utils.uploaded_track.UploadedTrackTestFilename import UploadedTrackTestFilename


class TextCase(UploadedTrackTestCase):
    def test_random_then_ok(self):
        response = self._post_uploaded_track(UploadedTrackTestFilename.RECORDING_KEMAR_FRANCE_MP3)
        assert response.status_code == status.HTTP_201_CREATED
