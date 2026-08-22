from rest_framework import status
from the_music_tree_api_kit.exception.validation.FieldValidationErrorCode import FieldValidationErrorCode
from the_music_tree_api_kit.utils.data_transformer import to_camel_case

from hear.serializer.model.uploaded_track.input.UploadedTrackInputFieldKey import UploadedTrackInputFieldKey
from hear.test.tests.integration.uploaded_track.UploadedTrackTestCase import UploadedTrackTestCase
from hear.test.utils.uploaded_track.UploadedTrackTestFilename import UploadedTrackTestFilename


class TestCase(UploadedTrackTestCase):
    def test_album_in_both_then_take_from_data(self):
        data_album_name = "Best of"
        data_dict = {
            UploadedTrackInputFieldKey.ALBUM_NAME.value: data_album_name,
            UploadedTrackInputFieldKey.ALBUM_ARTISTS_NAMES_MULTIPART.value: ["Muse"],
        }
        response = self._post_uploaded_track(UploadedTrackTestFilename.METADATA_LONG_A_ID3V1_SMALL_MP3, **data_dict)

        assert response.status_code == status.HTTP_201_CREATED
        album = self.saved_object.album
        assert album
        assert album.name == data_album_name

    def test_album_and_album_artists_in_data_and_only_album_in_metadata_then_take_from_data(self):
        data_album_name = "Best of"
        data_artist_name = "Muse"
        data = {
            UploadedTrackInputFieldKey.ALBUM_NAME.value: data_album_name,
            UploadedTrackInputFieldKey.ALBUM_ARTISTS_NAMES_MULTIPART.value: [data_artist_name],
        }
        response = self._post_uploaded_track(UploadedTrackTestFilename.ALBUM_KOKO_ID3V2_MP3, **data)

        assert response.status_code == status.HTTP_201_CREATED
        album = self.saved_object.album
        assert album
        assert album.name == data_album_name
        album_artist = album.album_artists.first()
        assert album_artist
        assert album_artist.name == data_artist_name

    def test_album_and_album_artists_in_data_and_metadata_then_take_from_data(self):
        data_album_name = "non"
        data_album_artists_str = "oiuhgoi efe"
        data_dict = {
            UploadedTrackInputFieldKey.ALBUM_NAME.value: data_album_name,
            UploadedTrackInputFieldKey.ALBUM_ARTISTS_NAMES_MULTIPART.value: data_album_artists_str,
        }
        response = self._post_uploaded_track(UploadedTrackTestFilename.METADATA_LONG_A_ID3V2_SMALL_MP3, **data_dict)

        assert response.status_code == status.HTTP_201_CREATED
        album = self.saved_object.album
        assert album
        assert album.name == data_album_name
        album_artist = album.album_artists.first()
        assert album_artist
        assert album_artist.name == data_album_artists_str

    def test_only_album_artists_in_data_and_album_in_metadata_then_400_bad_request(self):
        data_album_artists_name = "Muse"
        data = {UploadedTrackInputFieldKey.ALBUM_ARTISTS_NAMES_MULTIPART.value: [data_album_artists_name]}
        response = self._post_uploaded_track(UploadedTrackTestFilename.METADATA_LONG_A_ID3V2_SMALL_MP3, **data)

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        error = self.bad_request_result_field_errors[0]
        assert error["field"] == to_camel_case(UploadedTrackInputFieldKey.ALBUM_NAME)
        assert error["code"] == FieldValidationErrorCode.DEPENDENCY_MISSING

    def test_only_album_name_in_data_and_album_artists_in_metadata_then_201_created(self):
        data_album_name = "Best of"
        data = {UploadedTrackInputFieldKey.ALBUM_NAME.value: data_album_name}
        response = self._post_uploaded_track(UploadedTrackTestFilename.METADATA_LONG_A_ID3V1_SMALL_MP3, **data)

        assert response.status_code == status.HTTP_201_CREATED
        album = self.saved_object.album
        assert album
        assert album.name == data_album_name
