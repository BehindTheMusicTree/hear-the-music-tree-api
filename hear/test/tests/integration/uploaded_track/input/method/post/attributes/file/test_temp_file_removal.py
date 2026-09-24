from pathlib import Path

from rest_framework import status

from hear import settings
from hear.test.tests.integration.uploaded_track.UploadedTrackTestCase import UploadedTrackTestCase
from hear.test.utils.uploaded_track.UploadedTrackTestFilename import UploadedTrackTestFilename


class TestCase(UploadedTrackTestCase):
    def test_uploaded_track_created_then_temp_dir_empty(self):
        assert list(Path(settings.FILE_UPLOAD_TEMP_DIR).iterdir()) == []

        response = self._post_uploaded_track(UploadedTrackTestFilename.DEFAULT_MP3)

        assert response.status_code == status.HTTP_201_CREATED
        assert list(Path(settings.FILE_UPLOAD_TEMP_DIR).iterdir()) == []

    def test_uploaded_track_post_in_400_then_temp_dir_empty(self):
        assert list(Path(settings.FILE_UPLOAD_TEMP_DIR).iterdir()) == []

        response = self._post_uploaded_track(UploadedTrackTestFilename.FORMAT_CORRUPTED_WAV)

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert list(Path(settings.FILE_UPLOAD_TEMP_DIR).iterdir()) == []
