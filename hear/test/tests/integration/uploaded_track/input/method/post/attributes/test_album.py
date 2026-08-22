from rest_framework import status

from hear.test.tests.integration.uploaded_track.UploadedTrackTestCase import UploadedTrackTestCase
from hear.test.utils.uploaded_track.UploadedTrackTestFilename import UploadedTrackTestFilename


class TestCase(UploadedTrackTestCase):
    def test_not_povided_then_none(self):
        response = self._post_uploaded_track(UploadedTrackTestFilename.METADATA_NONE_MP3)
        assert response.status_code == status.HTTP_201_CREATED
        assert self.saved_object.album == None
