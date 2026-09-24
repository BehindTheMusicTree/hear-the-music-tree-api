from hear.serializer.model.uploaded_track.input.UploadedTrackInputFieldKey import UploadedTrackInputFieldKey
from hear.test.tests.integration.uploaded_track.UploadedTrackTestCase import UploadedTrackTestCase
from hear.test.utils.uploaded_track.UploadedTrackTestFilename import UploadedTrackTestFilename
from hear.utils.audio_file_metadata.AppMetadataKey import AppMetadataKey


class TestCase(UploadedTrackTestCase):
    def test_none_then_none_on_empty_mp3(self):
        response = self._post_uploaded_track(
            UploadedTrackTestFilename.METADATA_NONE_MP3, **{UploadedTrackInputFieldKey.RATING.value: None}
        )
        assert response.status_code == 201
        assert not self.saved_uploaded_track_metadata_with_raw_rating.get(AppMetadataKey.RATING, None)

    def test_none_then_none_on_empty_wav(self):
        response = self._post_uploaded_track(
            UploadedTrackTestFilename.METADATA_NONE_WAV, **{UploadedTrackInputFieldKey.RATING.value: None}
        )
        assert response.status_code == 201
        assert not self.saved_uploaded_track_metadata_with_raw_rating.get(AppMetadataKey.RATING, None)

    def test_none_then_none_on_empty_flac(self):
        response = self._post_uploaded_track(
            UploadedTrackTestFilename.METADATA_NONE_FLAC, **{UploadedTrackInputFieldKey.RATING.value: None}
        )
        assert response.status_code == 201
        assert not self.saved_uploaded_track_metadata_with_raw_rating.get(AppMetadataKey.RATING, None)

    def test_none_then_none_on_filled_mp3(self):
        response = self._post_uploaded_track(
            UploadedTrackTestFilename.METADATA_LONG_A_ID3V2_SMALL_MP3, **{UploadedTrackInputFieldKey.RATING.value: None}
        )
        assert response.status_code == 201
        assert not self.saved_uploaded_track_metadata_with_raw_rating.get(AppMetadataKey.RATING, None)

    def test_none_then_none_on_filled_wav(self):
        response = self._post_uploaded_track(
            UploadedTrackTestFilename.METADATA_LONG_A_ID3V2_SMALL_WAV, **{UploadedTrackInputFieldKey.RATING.value: None}
        )
        assert response.status_code == 201
        assert not self.saved_uploaded_track_metadata_with_raw_rating.get(AppMetadataKey.RATING, None)

    def test_none_then_none_on_filled_flac(self):
        response = self._post_uploaded_track(
            UploadedTrackTestFilename.METADATA_LONG_A_VORBIS_SMALL_FLAC,
            **{UploadedTrackInputFieldKey.RATING.value: None},
        )
        assert response.status_code == 201
        assert not self.saved_uploaded_track_metadata_with_raw_rating.get(AppMetadataKey.RATING, None)

    def test_10_then_10_on_empty_mp3(self):
        response = self._post_uploaded_track(
            UploadedTrackTestFilename.METADATA_NONE_MP3, **{UploadedTrackInputFieldKey.RATING.value: 10}
        )
        assert response.status_code == 201
        assert self.saved_uploaded_track_metadata_with_raw_rating[AppMetadataKey.RATING] == 255

    def test_10_then_10_on_empty_wav(self):
        response = self._post_uploaded_track(
            UploadedTrackTestFilename.METADATA_NONE_WAV, **{UploadedTrackInputFieldKey.RATING.value: 10}
        )
        assert response.status_code == 201
        assert self.saved_uploaded_track_metadata_with_raw_rating[AppMetadataKey.RATING] == 255

    def test_10_then_10_on_empty_flac(self):
        response = self._post_uploaded_track(
            UploadedTrackTestFilename.METADATA_NONE_FLAC, **{UploadedTrackInputFieldKey.RATING.value: 10}
        )
        assert response.status_code == 201
        assert self.saved_uploaded_track_metadata_with_raw_rating[AppMetadataKey.RATING] == 100

    def test_10_then_10_on_filled_mp3(self):
        response = self._post_uploaded_track(
            UploadedTrackTestFilename.METADATA_LONG_A_ID3V1_SMALL_MP3, **{UploadedTrackInputFieldKey.RATING.value: 10}
        )
        assert response.status_code == 201
        assert self.saved_uploaded_track_metadata_with_raw_rating[AppMetadataKey.RATING] == 255

    def test_10_then_10_on_filled_wav(self):
        response = self._post_uploaded_track(
            UploadedTrackTestFilename.METADATA_LONG_A_RIFF_SMALL_WAV, **{UploadedTrackInputFieldKey.RATING.value: 10}
        )
        assert response.status_code == 201
        assert self.saved_uploaded_track_metadata_with_raw_rating[AppMetadataKey.RATING] == 255

    def test_10_then_10_on_filled_flac(self):
        response = self._post_uploaded_track(
            UploadedTrackTestFilename.METADATA_LONG_A_VORBIS_SMALL_FLAC, **{UploadedTrackInputFieldKey.RATING.value: 10}
        )
        assert response.status_code == 201
        assert self.saved_uploaded_track_metadata_with_raw_rating[AppMetadataKey.RATING] == 100
