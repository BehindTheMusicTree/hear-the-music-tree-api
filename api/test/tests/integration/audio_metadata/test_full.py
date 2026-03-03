import os

from api import settings
from rest_framework import status
from api.test.tests.integration.audio_metadata.AudioMetadataTestCase import AudioMetadataTestCase
from api.test.utils.uploaded_track.UploadedTrackTestFilename import UploadedTrackTestFilename


class TestCase(AudioMetadataTestCase):
    def test_post_audio_file_then_200_ok(self):
        response = self._post_get_full_metadata(
            test_uploaded_track_filename=UploadedTrackTestFilename.DEFAULT_MP3
        )
        assert response.status_code == status.HTTP_200_OK
        assert response.json() is not None

    def test_post_queen_recording_then_200_ok(self):
        response = self._post_get_full_metadata(
            test_uploaded_track_filename=UploadedTrackTestFilename.RECORDING_QUEEN_25_MATCHES_BUT_ONE_WITH_BEST_DURATION_AND_MOST_FIELDS_AND_MOST_RELEASE_GROUPS_MP3
        )
        assert response.status_code == status.HTTP_200_OK
        assert response.json() is not None

    def test_not_auth_then_ok(self):
        self._logout()
        response = self._post_get_full_metadata()
        assert response.status_code == status.HTTP_200_OK
        assert response.json() is not None

    def test_auth_then_ok(self):
        self._login_as_test_user1()
        response = self._post_get_full_metadata()
        assert response.status_code == status.HTTP_200_OK
        assert response.json() is not None

    def test_full_metadata_ok_then_temp_dir_empty(self):
        temp_dir = settings.FILE_UPLOAD_TEMP_DIR
        for name in os.listdir(temp_dir):
            os.unlink(os.path.join(temp_dir, name))
        assert os.listdir(temp_dir) == []

        response = self._post_get_full_metadata(
            test_uploaded_track_filename=UploadedTrackTestFilename.DEFAULT_MP3
        )

        assert response.status_code == status.HTTP_200_OK
        assert os.listdir(temp_dir) == []
