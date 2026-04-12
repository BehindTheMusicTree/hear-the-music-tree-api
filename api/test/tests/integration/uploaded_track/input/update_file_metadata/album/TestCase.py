from api import settings
from api.serializer.model.uploaded_track.input.UploadedTrackInputFieldKey import UploadedTrackInputFieldKey
from api.test.tests.integration.uploaded_track.input.update_file_metadata.UploadedTrackFileMetadataUpdateStrTestCase import (
    UploadedTrackFileMetadataUpdateStrTestCase,
)
from api.utils.audio_file_metadata.AppMetadataKey import AppMetadataKey


class TestCase(UploadedTrackFileMetadataUpdateStrTestCase):
    save_field = UploadedTrackInputFieldKey.ALBUM_NAME.value
    uploaded_track_app_metadata_key = AppMetadataKey.ALBUM_NAME
    length_max = settings.ALBUM_NAME_LEN_MAX
    album_artists_data = {UploadedTrackInputFieldKey.ALBUM_ARTISTS_NAMES_MULTIPART.value: ["Muse"]}

    def test_on_missing_tag_then_ok(self):
        self._test_value("a", additional_data=self.album_artists_data, file_has_metadata=False)

    def test_on_present_tag_then_ok(self):
        self._test_value("a", additional_data=self.album_artists_data, file_has_metadata=True)

    def test_largest_then_ok(self):
        self._test_value("a" * self.length_max, additional_data=self.album_artists_data, file_has_metadata=False)


class Mp3TestCase(TestCase):
    file_extension = ".mp3"


class FlacTestCase(TestCase):
    file_extension = ".flac"


class WavTestCase(TestCase):
    file_extension = ".wav"
