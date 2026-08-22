from rest_framework import status

from hear.serializer.model.uploaded_track.input.UploadedTrackInputFieldKey import UploadedTrackInputFieldKey
from hear.test.tests.integration.uploaded_track.UploadedTrackTestCase import UploadedTrackTestCase
from hear.test.utils.uploaded_track.UploadedTrackTestFilename import UploadedTrackTestFilename


class TestCase(UploadedTrackTestCase):
    def test_title_in_both_then_take_data(self):
        data_title = "Rock"
        data_dict = {UploadedTrackInputFieldKey.TITLE.value: data_title}
        response = self._post_uploaded_track(UploadedTrackTestFilename.METADATA_LONG_A_ID3V2_SMALL_MP3, **data_dict)

        assert response.status_code == status.HTTP_201_CREATED
        assert self.saved_object.title == data_title
