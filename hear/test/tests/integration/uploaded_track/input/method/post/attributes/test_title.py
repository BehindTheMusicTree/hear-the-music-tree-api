from unittest.mock import Mock, patch

from django.core.files.uploadedfile import TemporaryUploadedFile
from rest_framework import status

from hear import settings
from hear.test.tests.integration.uploaded_track.UploadedTrackTestCase import UploadedTrackTestCase
from hear.test.utils.uploaded_track.UploadedTrackDownloadTestUrl import UploadedTrackDownloadTestUrl
from hear.test.utils.uploaded_track.UploadedTrackTestFilename import UploadedTrackTestFilename


class TestCase(UploadedTrackTestCase):
    def test_not_povided_then_set_from_filename_without_dots(self):
        response = self._post_uploaded_track(UploadedTrackTestFilename.FILENAME_DOTNOTINFILENAME_MP3)

        assert response.status_code == status.HTTP_201_CREATED
        assert self.saved_object.title == "filename=dotnotinfilename"

    def test_not_povided_then_set_from_filename_with_dots(self):
        response = self._post_uploaded_track(UploadedTrackTestFilename.FILENAME_DOT_IN_FILENAME_MP3)

        assert response.status_code == status.HTTP_201_CREATED
        assert self.saved_object.title == "filename=dot.in.filename"

    def test_not_povided_then_set_from_filename_with_spaces_removing_extra_spaces(self):
        response = self._post_uploaded_track(UploadedTrackTestFilename.FILENAME_WITH_SPACES_MP3)

        assert response.status_code == status.HTTP_201_CREATED
        assert self.saved_object.title == "filename= with spaces"

    @patch("hear.serializer.field.TrackFileField.TrackFileField._download_file_from_url")
    @patch("requests.get")
    def test_not_providing_title_nor_artist_and_original_filename_too_long_then_generate_with_app_prefixe(
        self, mock_requests_get, mock_download
    ):
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.headers = {}
        mock_response.iter_content = lambda chunk_size: (b"",)
        mock_requests_get.return_value = mock_response

        long_filename = "x" * (settings.UPLOADED_TRACK_FILENAME_LEN_MAX + 1) + ".mp3"
        mp3_path = self.TEST_FILES_BASE_DIR / UploadedTrackTestFilename.METADATA_NONE_MP3.value
        with open(mp3_path, "rb") as f:
            mp3_bytes = f.read()
        temp_file = TemporaryUploadedFile(
            name=long_filename,
            content_type="audio/mpeg",
            size=len(mp3_bytes),
            charset=None,
        )
        temp_file.write(mp3_bytes)
        temp_file.seek(0)
        mock_download.return_value = temp_file

        response = self._post_uploaded_track_from_url(UploadedTrackDownloadTestUrl.LONG_MP3)

        assert response.status_code == status.HTTP_201_CREATED
        assert self.saved_object.title.startswith(settings.UPLOADED_TRACK_GENERATED_TITLE_PREFIXE)
