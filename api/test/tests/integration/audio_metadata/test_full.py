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
