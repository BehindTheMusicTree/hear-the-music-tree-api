from rest_framework import status

from api import settings
from api.exception.validation.FieldValidationErrorCode import FieldValidationErrorCode
from api.serializer.model.uploaded_track.input.UploadedTrackInputFieldKey import UploadedTrackInputFieldKey
from api.test.utils.field.body_data.type.NullableCharBodyDataTestCase import NullableCharBodyDataTestCase
from api.test.utils.uploaded_track.UploadedTrackTestFilename import UploadedTrackTestFilename
from api.test.tests.integration.uploaded_track.UploadedTrackTestCase import UploadedTrackTestCase
from api.utils.data_transformer import to_camel_case


class TestCase(UploadedTrackTestCase, NullableCharBodyDataTestCase):

    def test_largest_then_ok(self):
        album_name = "a" * settings.ALBUM_NAME_LEN_MAX
        data = {
            UploadedTrackInputFieldKey.ALBUM_NAME.value: album_name,
            UploadedTrackInputFieldKey.ALBUM_ARTISTS_NAMES_MULTIPART.value: ["muse"],
        }
        response = self._post_uploaded_track(UploadedTrackTestFilename.METADATA_NONE_MP3, **data)

        assert response.status_code == status.HTTP_201_CREATED
        assert self.saved_object.album
        assert self.saved_object.album.name == album_name

    def test_too_large_then_400_bad_request(self):
        album_name = "a" * (settings.ALBUM_NAME_LEN_MAX + 1)
        data = {
            UploadedTrackInputFieldKey.ALBUM_NAME.value: album_name,
            UploadedTrackInputFieldKey.ARTISTS_NAMES_MULTIPART.value: ["muse"],
        }
        response = self._post_uploaded_track(UploadedTrackTestFilename.METADATA_NONE_MP3, **data)

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert len(self.bad_request_result_field_errors) == 1
        error = self.bad_request_result_field_errors[0]
        assert error['field'] == to_camel_case(UploadedTrackInputFieldKey.ALBUM_NAME)
        assert error['code'] == FieldValidationErrorCode.STRING_TOO_LONG

    def test_empty_then_ok(self):
        response = self._post_uploaded_track(
            UploadedTrackTestFilename.METADATA_NONE_MP3,
            **{UploadedTrackInputFieldKey.ALBUM_NAME.value: ''},
        )

        assert response.status_code == status.HTTP_201_CREATED
        assert self.saved_object.album == None

    def test_existing_then_ok(self):
        album_name = "Kopoe"
        album = self.model_fixture_factory.create_album(name=album_name)

        data = {
            UploadedTrackInputFieldKey.ALBUM_NAME.value: album_name,
            UploadedTrackInputFieldKey.ALBUM_ARTISTS_NAMES_MULTIPART.value: [],
        }
        response = self._post_uploaded_track(
            test_uploaded_track_filename=UploadedTrackTestFilename.METADATA_NONE_MP3, **data)

        assert response.status_code == status.HTTP_201_CREATED
        assert self.saved_object.album
        assert self.saved_object.album.uuid == album.uuid

    def test_not_existing(self):
        album_name = "hoho"
        data = {
            UploadedTrackInputFieldKey.ALBUM_NAME.value: album_name,
            UploadedTrackInputFieldKey.ALBUM_ARTISTS_NAMES_MULTIPART.value: ["muse"],
        }
        response = self._post_uploaded_track(
            test_uploaded_track_filename=UploadedTrackTestFilename.METADATA_NONE_MP3, **data)

        assert response.status_code == status.HTTP_201_CREATED
        assert self.saved_object.album
        assert self.saved_object.album.name == album_name

    def test_multi_value_then_400_bad_request(self):
        data = {
            UploadedTrackInputFieldKey.ALBUM_NAME.value: ['a', 'b'],
            UploadedTrackInputFieldKey.ARTISTS_NAMES_MULTIPART.value: ["muse"],
        }
        response = self._post_uploaded_track(UploadedTrackTestFilename.METADATA_NONE_MP3, **data)

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert len(self.bad_request_result_field_errors) == 1
        error = self.bad_request_result_field_errors[0]
        assert error['field'] == to_camel_case(UploadedTrackInputFieldKey.ALBUM_NAME)
        assert error['code'] == FieldValidationErrorCode.DUPLICATE
