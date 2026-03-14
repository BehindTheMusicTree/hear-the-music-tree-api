import pytest
from rest_framework import status

from api.exception.validation.FieldValidationErrorCode import FieldValidationErrorCode
from api.serializer.model.uploaded_track.input.UploadedTrackInputFieldKey import UploadedTrackInputFieldKey
from api.test.utils.uploaded_track.UploadedTrackTestFilename import UploadedTrackTestFilename
from api.test.tests.integration.uploaded_track.UploadedTrackTestCase import UploadedTrackTestCase


class TestCase(UploadedTrackTestCase):

    def test_duplicate_fingerprint_and_must_cancel_if_duplicate_fingerprint_then_bad_request(self):
        data = {UploadedTrackInputFieldKey.TRACK_FILE_FINGERPRINT_MUST_BE_UNIQUE.value: True}
        response = self._post_uploaded_track(UploadedTrackTestFilename.RECORDING_KEMAR_FRANCE_MP3, **data)

        assert response.status_code == status.HTTP_201_CREATED

        response = self._post_uploaded_track(UploadedTrackTestFilename.RECORDING_KEMAR_FRANCE_MP3, **data)

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert len(self.bad_request_result_field_errors) == 1
        error = self.bad_request_result_field_errors[0]
        assert error['field'] == UploadedTrackInputFieldKey.TRACK_FILE_PUBLIC.value
        assert error['code'] == FieldValidationErrorCode.TRACK_FILE_FINGERPRINT_DUPLICATE

    def test_not_duplicate_fingerprint_and_must_cancel_if_duplicate_fingerprint_then_ok(self):
        data = {UploadedTrackInputFieldKey.TRACK_FILE_FINGERPRINT_MUST_BE_UNIQUE.value: True}
        response = self._post_uploaded_track(UploadedTrackTestFilename.METADATA_NONE_MP3, **data)

        assert response.status_code == status.HTTP_201_CREATED

        response = self._post_uploaded_track(UploadedTrackTestFilename.RECORDING_SHOWMUSTGOON_MP3, **data)

        assert response.status_code == status.HTTP_201_CREATED

    def test_duplicate_fingerprint_and_not_must_cancel_if_duplicate_fingerprint_then_ok(self):
        data = {UploadedTrackInputFieldKey.TRACK_FILE_FINGERPRINT_MUST_BE_UNIQUE.value: False}
        response = self._post_uploaded_track(UploadedTrackTestFilename.METADATA_NONE_MP3, **data)

        assert response.status_code == status.HTTP_201_CREATED

        response = self._post_uploaded_track(UploadedTrackTestFilename.METADATA_NONE_MP3, **data)

        assert response.status_code == status.HTTP_201_CREATED

    def test_duplicate_fingerprint_and_must_cancel_if_duplicate_fingerprint_not_provided_then_ok(self):
        data = {UploadedTrackInputFieldKey.TRACK_FILE_FINGERPRINT_MUST_BE_UNIQUE.value: False}
        response = self._post_uploaded_track(UploadedTrackTestFilename.METADATA_NONE_MP3, **data)

        assert response.status_code == status.HTTP_201_CREATED

        response = self._post_uploaded_track(UploadedTrackTestFilename.METADATA_NONE_MP3, **data)

        assert response.status_code == status.HTTP_201_CREATED
