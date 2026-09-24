from rest_framework import status
from the_music_tree_api_kit.exception.validation.FieldValidationErrorCode import FieldValidationErrorCode

from hear.serializer.model.uploaded_track.input.UploadedTrackInputFieldKey import UploadedTrackInputFieldKey
from hear.test.tests.integration.uploaded_track.UploadedTrackTestCase import UploadedTrackTestCase
from hear.test.utils.uploaded_track.UploadedTrackTestFilename import UploadedTrackTestFilename
from hear.utils import audio_file_metadata


class TestCase(UploadedTrackTestCase):
    def test_flac_md5_not_valid_and_corrupted_then_400_bad_request(self):
        response = self._post_uploaded_track(UploadedTrackTestFilename.FORMAT_MD5_NOT_VALID_AND_CORRUPTED_FLAC)

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert len(self.bad_request_result_field_errors) == 1
        error = self.bad_request_result_field_errors[0]
        assert error["field"] == UploadedTrackInputFieldKey.TRACK_FILE_PUBLIC.value
        assert error["code"] == FieldValidationErrorCode.TRACK_FILE_CORRUPTED

    def test_flac_md5_not_valid_not_because_of_id3v1_metadata_then_corrected(self):
        response = self._post_uploaded_track(
            UploadedTrackTestFilename.FORMAT_MD5_NOT_VALID_NOT_BECAUSE_OF_ID3V1_METADATA_FLAC
        )

        assert response.status_code == status.HTTP_201_CREATED
        assert self.saved_object.track_file.md5_has_been_corrected
        assert audio_file_metadata.is_flac_md5_valid(self.saved_object.track_file.file)

    def test_flac_md5_not_valid_because_of_id3v1_metadata_then_corrected(self):
        response = self._post_uploaded_track(
            UploadedTrackTestFilename.FORMAT_MD5_NOT_VALID_BECAUSE_OF_ID3V1_METADATA_FLAC
        )

        assert response.status_code == status.HTTP_201_CREATED
        assert self.saved_object.track_file.md5_has_been_corrected

    def test_flac_md5_is_valid(self):
        response = self._post_uploaded_track(UploadedTrackTestFilename.RECORDING_DANS_LA_LEGENDE_FLAC)

        assert response.status_code == status.HTTP_201_CREATED
        assert self.saved_object.track_file
        assert not self.saved_object.track_file.md5_has_been_corrected
