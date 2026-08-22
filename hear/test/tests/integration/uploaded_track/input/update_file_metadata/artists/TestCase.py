from hear import settings
from hear.serializer.model.uploaded_track.input.UploadedTrackInputFieldKey import UploadedTrackInputFieldKey
from hear.test.tests.integration.uploaded_track.input.update_file_metadata.UploadedTrackFileMetadataUpdateStrTestCase import (
    UploadedTrackFileMetadataUpdateStrTestCase,
)
from hear.utils.audio_file_metadata.AppMetadataKey import AppMetadataKey


class TestCase(UploadedTrackFileMetadataUpdateStrTestCase):
    save_field = UploadedTrackInputFieldKey.ARTISTS_NAMES_MULTIPART.value
    uploaded_track_app_metadata_key = AppMetadataKey.ARTISTS_NAMES
    length_max = settings.ARTIST_NAME_LEN_MAX
    value_expected_in_metadata_is_list = True


class Mp3TestCase(TestCase):
    file_extension = ".mp3"


class FlacTestCase(TestCase):
    file_extension = ".flac"


class WavTestCase(TestCase):
    file_extension = ".wav"
