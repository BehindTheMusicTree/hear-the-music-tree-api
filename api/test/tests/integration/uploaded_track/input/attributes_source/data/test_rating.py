from rest_framework import status

from api.serializer.model.uploaded_track.input.UploadedTrackInputFieldKey import UploadedTrackInputFieldKey
from api.test.utils.uploaded_track.UploadedTrackTestFilename import UploadedTrackTestFilename
from api.test.tests.integration.uploaded_track.UploadedTrackTestCase import UploadedTrackTestCase


class RatingTestCase(UploadedTrackTestCase):

    def test_value_then_ok(self):
        value = 1
        response = self._post_uploaded_track(UploadedTrackTestFilename.METADATA_NONE_MP3, **{UploadedTrackInputFieldKey.RATING: value})

        assert response.status_code == status.HTTP_201_CREATED
        assert self.saved_object.rating == value

    def test_empty_then_none(self):
        response = self._post_uploaded_track(UploadedTrackTestFilename.METADATA_NONE_MP3, **{UploadedTrackInputFieldKey.RATING: ""})

        assert response.status_code == status.HTTP_201_CREATED
        assert self.saved_object.rating == None
