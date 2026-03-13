from rest_framework import status

from api.serializer.model.uploaded_track.input.UploadedTrackInputFieldKey import UploadedTrackInputFieldKey
from api.test.utils.uploaded_track.UploadedTrackTestFilename import UploadedTrackTestFilename
from api.test.tests.integration.uploaded_track.UploadedTrackTestCase import UploadedTrackTestCase


class TestCase(UploadedTrackTestCase):

    def test_rating_in_both_then_take_data(self):
        data_rating = 7
        response = self._post_uploaded_track(UploadedTrackTestFilename.RATING_ID3V2_1_STAR_MP3,
                                             **{UploadedTrackInputFieldKey.RATING: data_rating})

        assert response.status_code == status.HTTP_201_CREATED
        assert self.saved_object.rating == data_rating
