from rest_framework import status

from hear.serializer.model.uploaded_track.input.UploadedTrackInputFieldKey import UploadedTrackInputFieldKey
from hear.test.tests.integration.uploaded_track.UploadedTrackTestCase import UploadedTrackTestCase
from hear.test.utils.uploaded_track.UploadedTrackTestFilename import UploadedTrackTestFilename


class LanguageTestCase(UploadedTrackTestCase):
    def test_value_then_ok(self):
        value = "fr"
        response = self._post_uploaded_track(
            UploadedTrackTestFilename.METADATA_NONE_MP3, **{UploadedTrackInputFieldKey.LANGUAGE.value: value}
        )

        assert response.status_code == status.HTTP_201_CREATED
        assert self.saved_object.language == value

    def test_empty_then_none(self):
        response = self._post_uploaded_track(
            UploadedTrackTestFilename.METADATA_NONE_MP3, **{UploadedTrackInputFieldKey.LANGUAGE.value: ""}
        )

        assert response.status_code == status.HTTP_201_CREATED
        assert self.saved_object.language == None
