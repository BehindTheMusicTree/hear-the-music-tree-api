from rest_framework import status

from api.serializer.model.uploaded_track.input.UploadedTrackInputFieldKey import UploadedTrackInputFieldKey
from api.test.tests.integration.uploaded_track.UploadedTrackTestCase import UploadedTrackTestCase
from api.test.utils.uploaded_track.UploadedTrackTestFilename import UploadedTrackTestFilename


class TestCase(UploadedTrackTestCase):
    def test_value_then_ok(self):
        value = "rovk"
        response = self._post_uploaded_track(
            UploadedTrackTestFilename.METADATA_NONE_MP3, **{UploadedTrackInputFieldKey.GENRE.value: value}
        )
        assert response.status_code == status.HTTP_201_CREATED
        genre = self.saved_object.genre
        assert genre
        assert genre.name == value

    def test_empty_then_none(self):
        response = self._post_uploaded_track(
            UploadedTrackTestFilename.METADATA_NONE_MP3, **{UploadedTrackInputFieldKey.GENRE.value: ""}
        )
        assert response.status_code == status.HTTP_201_CREATED
        assert self.saved_object.genre == None
