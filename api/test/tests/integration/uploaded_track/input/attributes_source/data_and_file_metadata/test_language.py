from rest_framework import status

from api.serializer.model.uploaded_track.input.UploadedTrackInputFieldKey import UploadedTrackInputFieldKey
from api.test.tests.integration.uploaded_track.UploadedTrackTestCase import UploadedTrackTestCase
from api.test.utils.uploaded_track.UploadedTrackTestFilename import UploadedTrackTestFilename


class TestCase(UploadedTrackTestCase):
    def test_title_in_both_then_take_data(self):
        data_language = "fr"
        data_dict = {UploadedTrackInputFieldKey.LANGUAGE.value: data_language}
        response = self._post_uploaded_track(UploadedTrackTestFilename.METADATA_LONG_A_ID3V2_SMALL_MP3, **data_dict)

        assert response.status_code == status.HTTP_201_CREATED
        assert self.saved_object.language == data_language
