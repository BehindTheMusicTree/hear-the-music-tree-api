from rest_framework import status
from api.test.tests.integration.audio_metadata.AudioMetadataTestCase import AudioMetadataTestCase
from serializer.audio_metadata.Fields import Fields


class TestCase(AudioMetadataTestCase):
    def test_ok(self):
        response = self._post_get_full_metadata()
        assert response.status_code == status.HTTP_200_OK
        assert self.result is not None
