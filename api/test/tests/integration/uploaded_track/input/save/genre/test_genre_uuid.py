from rest_framework import status

from api.exception.validation.FieldValidationErrorCode import FieldValidationErrorCode
from api.serializer.model.uploaded_track.input.UploadedTrackInputFieldKey import UploadedTrackInputFieldKey
from api.test.utils.field.body_data.type.ForeignKeyBodyDataTestCase import ForeignKeyBodyDataTestCase
from api.test.utils.uploaded_track.UploadedTrackTestFilename import UploadedTrackTestFilename
from api.test.tests.integration.uploaded_track.UploadedTrackTestCase import UploadedTrackTestCase


class TestCase(ForeignKeyBodyDataTestCase, UploadedTrackTestCase):

    def test_non_existing_then_400_bad_request(self):
        non_exisintg_uuid = "00000000-0000-0000-0000-000000000000"
        response = self._post_uploaded_track(UploadedTrackTestFilename.METADATA_NONE_MP3,
                                             **{UploadedTrackInputFieldKey.GENRE: non_exisintg_uuid})

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert len(self.bad_request_result_field_errors) == 1
        error = self.bad_request_result_field_errors[0]
        assert error['field'] == UploadedTrackInputFieldKey.GENRE.value
        assert error['code'] == FieldValidationErrorCode.REFERENCE_INVALID

    def test_existing_then_ok(self):
        genre = self.model_fixture_factory.create_genre(name="rock")
        response = self._post_uploaded_track(
            UploadedTrackTestFilename.METADATA_NONE_MP3, **{UploadedTrackInputFieldKey.GENRE: genre.uuid})

        assert response.status_code == status.HTTP_201_CREATED
        assert self.saved_object
        assert self.saved_object.genre == genre

    def test_empty_then_none(self):
        response = self._post_uploaded_track(UploadedTrackTestFilename.METADATA_NONE_MP3, **{UploadedTrackInputFieldKey.GENRE: ""})

        assert response.status_code == status.HTTP_201_CREATED
        assert self.saved_object.genre is None

    def test_multi_value_then_400_bad_request(self):
        genre = self.model_fixture_factory.create_genre(name="rock")

        response = self._post_uploaded_track(
            UploadedTrackTestFilename.METADATA_NONE_MP3, **{UploadedTrackInputFieldKey.GENRE: [genre.uuid, genre.uuid]})

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert len(self.bad_request_result_field_errors) == 1
        error = self.bad_request_result_field_errors[0]
        assert error['field'] == UploadedTrackInputFieldKey.GENRE.value
        assert error['code'] == FieldValidationErrorCode.DUPLICATE

    def test_invalid_uuid_then_400_bad_request(self):
        invalid_uuid = "036aa19e-d5ae-425a-93f2-125ccd145a15"
        response = self._post_uploaded_track(
            UploadedTrackTestFilename.METADATA_NONE_MP3, **{UploadedTrackInputFieldKey.GENRE: invalid_uuid})

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert len(self.bad_request_result_field_errors) == 1
        error = self.bad_request_result_field_errors[0]
        assert error['field'] == UploadedTrackInputFieldKey.GENRE.value
        assert error['code'] == FieldValidationErrorCode.REFERENCE_INVALID
