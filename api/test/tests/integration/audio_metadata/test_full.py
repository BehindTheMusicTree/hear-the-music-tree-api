import os

from api import settings
from rest_framework import status
from api.test.tests.integration.audio_metadata.AudioMetadataTestCase import AudioMetadataTestCase


class TestCase(AudioMetadataTestCase):
    def test_ok(self):
        response = self._post_get_full_metadata()
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
        assert os.listdir(settings.FILE_UPLOAD_TEMP_DIR) == []

        response = self._post_get_full_metadata()

        assert response.status_code == status.HTTP_200_OK
        assert os.listdir(settings.FILE_UPLOAD_TEMP_DIR) == []
