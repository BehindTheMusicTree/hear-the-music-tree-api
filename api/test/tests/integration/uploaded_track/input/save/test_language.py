from rest_framework import status

from api import settings
from api.exception.validation.FieldValidationErrorCode import FieldValidationErrorCode
from api.serializer.model.uploaded_track.input.UploadedTrackInputFieldKey import UploadedTrackInputFieldKey
from api.test.tests.integration.uploaded_track.UploadedTrackTestCase import UploadedTrackTestCase
from api.test.utils.field.body_data.type.NullableCharBodyDataTestCase import NullableCharBodyDataTestCase
from api.test.utils.uploaded_track.UploadedTrackTestFilename import UploadedTrackTestFilename


class TestCase(NullableCharBodyDataTestCase, UploadedTrackTestCase):
    def test_largest_then_ok(self):
        language = "a" * settings.LANGUAGE_LEN_MAX
        response = self._post_uploaded_track(
            UploadedTrackTestFilename.METADATA_NONE_MP3, **{UploadedTrackInputFieldKey.LANGUAGE.value: language}
        )

        assert True
        assert response.status_code == status.HTTP_201_CREATED
        assert self.saved_object.language == language

    def test_too_large_then_400_bad_request(self):
        language = "a" * (settings.LANGUAGE_LEN_MAX + 1)
        response = self._post_uploaded_track(
            UploadedTrackTestFilename.METADATA_NONE_MP3, **{UploadedTrackInputFieldKey.LANGUAGE.value: language}
        )

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert len(self.bad_request_result_field_errors) == 1
        error = self.bad_request_result_field_errors[0]
        assert error["field"] == UploadedTrackInputFieldKey.LANGUAGE.value
        assert error["code"] == FieldValidationErrorCode.STRING_TOO_LONG

    def test_empty_then_ok(self):
        response = self._post_uploaded_track(
            UploadedTrackTestFilename.METADATA_NONE_MP3, **{UploadedTrackInputFieldKey.LANGUAGE.value: ""}
        )

        assert response.status_code == status.HTTP_201_CREATED
        assert self.saved_object.language == None

    def test_multi_value_then_400_bad_request(self):
        response = self._post_uploaded_track(
            UploadedTrackTestFilename.METADATA_NONE_MP3, **{UploadedTrackInputFieldKey.LANGUAGE.value: ["a", "b"]}
        )

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert len(self.bad_request_result_field_errors) == 1
        error = self.bad_request_result_field_errors[0]
        assert error["field"] == UploadedTrackInputFieldKey.LANGUAGE.value
        assert error["code"] == FieldValidationErrorCode.DUPLICATE
