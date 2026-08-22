from rest_framework import status

from hear.serializer.model.uploaded_track.input.UploadedTrackInputFieldKey import UploadedTrackInputFieldKey
from hear.test.tests.integration.uploaded_track.UploadedTrackTestCase import UploadedTrackTestCase
from hear.test.utils.uploaded_track.UploadedTrackTestFilename import UploadedTrackTestFilename


class TestCase(UploadedTrackTestCase):
    def test_value_then_ok(self):
        value = 1
        data = {
            UploadedTrackInputFieldKey.ALBUM_NAME.value: "albumito",
            UploadedTrackInputFieldKey.ALBUM_ARTISTS_NAMES_MULTIPART.value: [],
            UploadedTrackInputFieldKey.TRACK_NUMBER.value: value,
        }
        response = self._post_uploaded_track(UploadedTrackTestFilename.METADATA_NONE_MP3, **data)

        assert response.status_code == status.HTTP_201_CREATED
        assert self.saved_object.track_number == value

    def test_empty_then_none(self):
        data = {
            UploadedTrackInputFieldKey.ALBUM_NAME.value: "albumito",
            UploadedTrackInputFieldKey.ALBUM_ARTISTS_NAMES_MULTIPART.value: [],
            UploadedTrackInputFieldKey.TRACK_NUMBER.value: None,
        }
        response = self._post_uploaded_track(UploadedTrackTestFilename.METADATA_NONE_MP3, **data)

        assert response.status_code == status.HTTP_201_CREATED
        assert self.saved_object.track_number == None

    def test_not_provided_then_none(self):
        data = {
            UploadedTrackInputFieldKey.ALBUM_NAME.value: "albumito",
            UploadedTrackInputFieldKey.ALBUM_ARTISTS_NAMES_MULTIPART.value: [],
        }
        response = self._post_uploaded_track(UploadedTrackTestFilename.METADATA_NONE_MP3, **data)

        assert response.status_code == status.HTTP_201_CREATED
        assert self.saved_object.track_number == None
