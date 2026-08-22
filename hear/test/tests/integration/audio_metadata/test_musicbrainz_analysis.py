from unittest.mock import patch

from rest_framework import status
from the_music_tree_api_kit.utils.data_transformer import to_camel_case

from hear.serializer.audio_metadata.AudioMetadataFull import AudioMetadataFullSerializer
from hear.serializer.audio_metadata.Fields import Fields
from hear.test.tests.integration.audio_metadata.AudioMetadataTestCase import AudioMetadataTestCase
from hear.test.utils.uploaded_track.UploadedTrackTestFilename import UploadedTrackTestFilename
from hear.utils.audio_fingerprinter import service as audio_fingerprinter_service
from hear.utils.musicbrainz import service as musicbrainz_service

MUSICBRAINZ_RAW_DATA_CAMEL = to_camel_case("musicbrainz_raw_data")


def _force_include_musicbrainz_analysis_in_validated_data(serializer_class):
    """Patch serializer so validated_data includes include_musicbrainz_analysis=True after is_valid()."""
    original_is_valid = serializer_class.is_valid

    def patched_is_valid(self, raise_exception=False):
        result = original_is_valid(self, raise_exception=raise_exception)
        if hasattr(self, "_validated_data") and self._validated_data is not None:
            self._validated_data = dict(self._validated_data)
            self._validated_data[Fields.INCLUDE_MUSICBRAINZ_ANALYSIS] = True
        return result

    return patched_is_valid


class TestIncludeMusicbrainzAnalysisFalse(AudioMetadataTestCase):
    def test_include_musicbrainz_analysis_false_then_no_musicbrainz_raw_data(self):
        response = self._post_get_full_metadata(
            test_uploaded_track_filename=UploadedTrackTestFilename.DEFAULT_MP3,
            **{Fields.INCLUDE_MUSICBRAINZ_ANALYSIS: False},
        )
        assert response.status_code == status.HTTP_200_OK
        assert MUSICBRAINZ_RAW_DATA_CAMEL not in response.json()

    def test_include_musicbrainz_analysis_omitted_then_no_musicbrainz_raw_data(self):
        response = self._post_get_full_metadata(
            test_uploaded_track_filename=UploadedTrackTestFilename.DEFAULT_MP3,
        )
        assert response.status_code == status.HTTP_200_OK
        assert MUSICBRAINZ_RAW_DATA_CAMEL not in response.json()


class TestIncludeMusicbrainzAnalysisTrue(AudioMetadataTestCase):
    def test_include_musicbrainz_analysis_true_and_mb_match_then_raw_data_has_recording(self):
        mock_recording = {
            "id": "e2e-mock-recording-id",
            "title": "Mock Recording",
            "duration": 120,
            "score": 0.95,
            "artists": [{"id": "artist-1", "name": "Mock Artist"}],
        }
        with (
            patch.object(
                AudioMetadataFullSerializer,
                "is_valid",
                _force_include_musicbrainz_analysis_in_validated_data(AudioMetadataFullSerializer),
            ),
            patch("hear.utils.audio_fingerprinter.service.get_fingerprint_and_duration_for_analysis") as mock_fp,
            patch("hear.utils.musicbrainz.service.get_musicbrainz_recording_analysis") as mock_mb,
        ):
            mock_fp.return_value = {
                audio_fingerprinter_service.RESULT_FINGERPRINT: b"\x00" * 20,
                audio_fingerprinter_service.RESULT_DURATION_IN_SEC: 120.0,
                audio_fingerprinter_service.RESULT_ERROR_CODE: None,
                audio_fingerprinter_service.RESULT_ERROR_MESSAGE: None,
            }
            mock_mb.return_value = mock_recording
            response = self._post_get_full_metadata(
                test_uploaded_track_filename=UploadedTrackTestFilename.DEFAULT_MP3,
            )
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert MUSICBRAINZ_RAW_DATA_CAMEL in data
        raw = data[MUSICBRAINZ_RAW_DATA_CAMEL]
        assert raw["id"] == mock_recording["id"]
        assert raw["title"] == mock_recording["title"]
        assert raw["artists"] == mock_recording["artists"]
        assert raw["score"] == mock_recording["score"]

    def test_include_musicbrainz_analysis_true_and_mb_no_match_then_raw_data_has_error(self):
        error_payload = {
            musicbrainz_service.ANALYSIS_ERROR: musicbrainz_service.ERROR_NO_MATCH,
            musicbrainz_service.ANALYSIS_CODE: musicbrainz_service.ERROR_NO_MATCH,
            musicbrainz_service.ANALYSIS_MESSAGE: "No matching recording found.",
        }
        with (
            patch.object(
                AudioMetadataFullSerializer,
                "is_valid",
                _force_include_musicbrainz_analysis_in_validated_data(AudioMetadataFullSerializer),
            ),
            patch("hear.utils.audio_fingerprinter.service.get_fingerprint_and_duration_for_analysis") as mock_fp,
            patch("hear.utils.musicbrainz.service.get_musicbrainz_recording_analysis") as mock_mb,
        ):
            mock_fp.return_value = {
                audio_fingerprinter_service.RESULT_FINGERPRINT: b"\x00" * 20,
                audio_fingerprinter_service.RESULT_DURATION_IN_SEC: 120.0,
                audio_fingerprinter_service.RESULT_ERROR_CODE: None,
                audio_fingerprinter_service.RESULT_ERROR_MESSAGE: None,
            }
            mock_mb.return_value = error_payload
            response = self._post_get_full_metadata(
                test_uploaded_track_filename=UploadedTrackTestFilename.DEFAULT_MP3,
            )
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert MUSICBRAINZ_RAW_DATA_CAMEL in data
        raw = data[MUSICBRAINZ_RAW_DATA_CAMEL]
        assert raw["error"] == musicbrainz_service.ERROR_NO_MATCH
        assert "code" in raw
        assert "message" in raw

    def test_include_musicbrainz_analysis_true_and_fingerprint_fails_then_raw_data_has_error(self):
        with (
            patch.object(
                AudioMetadataFullSerializer,
                "is_valid",
                _force_include_musicbrainz_analysis_in_validated_data(AudioMetadataFullSerializer),
            ),
            patch("hear.utils.audio_fingerprinter.service.get_fingerprint_and_duration_for_analysis") as mock_fp,
        ):
            mock_fp.return_value = {
                audio_fingerprinter_service.RESULT_FINGERPRINT: None,
                audio_fingerprinter_service.RESULT_DURATION_IN_SEC: None,
                audio_fingerprinter_service.RESULT_ERROR_CODE: "timeout_error",
                audio_fingerprinter_service.RESULT_ERROR_MESSAGE: "Fingerprint request timed out.",
            }
            response = self._post_get_full_metadata(
                test_uploaded_track_filename=UploadedTrackTestFilename.DEFAULT_MP3,
            )
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert MUSICBRAINZ_RAW_DATA_CAMEL in data
        raw = data[MUSICBRAINZ_RAW_DATA_CAMEL]
        assert raw["error"] == "fingerprint_failed"
        assert raw["code"] == "timeout_error"
        assert raw["message"] == "Fingerprint request timed out."

    def test_include_musicbrainz_analysis_true_unauthenticated_then_200_and_raw_data(self):
        self._logout()
        mock_recording = {"id": "anon-recording", "title": "Anon", "artists": []}
        with (
            patch.object(
                AudioMetadataFullSerializer,
                "is_valid",
                _force_include_musicbrainz_analysis_in_validated_data(AudioMetadataFullSerializer),
            ),
            patch("hear.utils.audio_fingerprinter.service.get_fingerprint_and_duration_for_analysis") as mock_fp,
            patch("hear.utils.musicbrainz.service.get_musicbrainz_recording_analysis") as mock_mb,
        ):
            mock_fp.return_value = {
                audio_fingerprinter_service.RESULT_FINGERPRINT: b"\x00" * 20,
                audio_fingerprinter_service.RESULT_DURATION_IN_SEC: 60.0,
                audio_fingerprinter_service.RESULT_ERROR_CODE: None,
                audio_fingerprinter_service.RESULT_ERROR_MESSAGE: None,
            }
            mock_mb.return_value = mock_recording
            response = self._post_get_full_metadata(
                test_uploaded_track_filename=UploadedTrackTestFilename.DEFAULT_MP3,
            )
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert MUSICBRAINZ_RAW_DATA_CAMEL in data
        assert data[MUSICBRAINZ_RAW_DATA_CAMEL]["id"] == "anon-recording"
