from unittest.mock import patch

import pytest

from api.utils.musicbrainz.service import (
    ANALYSIS_CODE,
    ANALYSIS_ERROR,
    ANALYSIS_MESSAGE,
    ERROR_DURATION_TOO_SHORT,
    ERROR_NO_MATCH,
    get_musicbrainz_recording_analysis,
)


class TestGetMusicbrainzRecordingAnalysisSuccess:
    def test_valid_fingerprint_and_duration_then_returns_recording_dict(self):
        recording_dict = {
            "id": "rec-123",
            "title": "Test Track",
            "duration": 180,
            "score": 0.98,
            "artists": [{"id": "a1", "name": "Artist"}],
        }
        with patch(
            "api.utils.musicbrainz.service._get_musicbrainz_best_recording_dict_from_fingerprint_and_duration",
            return_value=recording_dict,
        ):
            result = get_musicbrainz_recording_analysis(
                fingerprint=b"\x00" * 20, duration_in_sec=180.0
            )
        assert result == recording_dict
        assert result["id"] == "rec-123"
        assert result["title"] == "Test Track"


class TestGetMusicbrainzRecordingAnalysisNoMatch:
    def test_lookup_returns_none_then_error_dict(self):
        with patch(
            "api.utils.musicbrainz.service._get_musicbrainz_best_recording_dict_from_fingerprint_and_duration",
            return_value=None,
        ):
            result = get_musicbrainz_recording_analysis(
                fingerprint=b"\x00" * 20, duration_in_sec=120.0
            )
        assert result[ANALYSIS_ERROR] == ERROR_NO_MATCH
        assert result[ANALYSIS_CODE] == ERROR_NO_MATCH
        assert "message" in result


class TestGetMusicbrainzRecordingAnalysisDuration:
    def test_duration_below_or_equal_1_sec_then_error_dict(self):
        result = get_musicbrainz_recording_analysis(
            fingerprint=b"\x00" * 20, duration_in_sec=1.0
        )
        assert result[ANALYSIS_ERROR] == ERROR_DURATION_TOO_SHORT
        assert result[ANALYSIS_CODE] == ERROR_DURATION_TOO_SHORT
        assert "message" in result

    def test_duration_above_1_sec_then_calls_lookup(self):
        with patch(
            "api.utils.musicbrainz.service._get_musicbrainz_best_recording_dict_from_fingerprint_and_duration",
            return_value={"id": "x", "title": "Y"},
        ) as mock_lookup:
            get_musicbrainz_recording_analysis(
                fingerprint=b"\x00" * 20, duration_in_sec=2.0
            )
        mock_lookup.assert_called_once()


class TestGetMusicbrainzRecordingAnalysisNoApiKey:
    def test_empty_acoustid_api_key_then_error_dict(self):
        with patch("api.utils.musicbrainz.service.settings") as mock_settings:
            mock_settings.ACOUSTID_API_KEY = ""
            result = get_musicbrainz_recording_analysis(
                fingerprint=b"\x00" * 20, duration_in_sec=120.0
            )
        assert result[ANALYSIS_ERROR] == "no_acoustid_api_key"
        assert ANALYSIS_MESSAGE in result
