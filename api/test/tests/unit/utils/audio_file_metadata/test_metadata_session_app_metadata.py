import pytest

from api.utils.audio_file_metadata.AppMetadataKey import AppMetadataKey
from api.utils.audio_file_metadata.metadata_session_app_metadata import (
    build_app_metadata_from_payload,
)


class TestBuildAppMetadataFromPayload:
    def test_empty_payload_then_empty_app_metadata(self):
        assert build_app_metadata_from_payload({}) == {}

    def test_title_only_then_single_key(self):
        result = build_app_metadata_from_payload({"title": "New Title"})
        assert result == {AppMetadataKey.TITLE: "New Title"}

    def test_multiple_fields_then_all_mapped(self):
        payload = {
            "title": "Track",
            "artists_names": ["A", "B"],
            "album_name": "Album",
            "album_artists_names": ["C"],
            "genres_names": ["Rock"],
            "rating": 80,
            "language": "en",
        }
        result = build_app_metadata_from_payload(payload)
        assert result[AppMetadataKey.TITLE] == "Track"
        assert result[AppMetadataKey.ARTISTS_NAMES] == ["A", "B"]
        assert result[AppMetadataKey.ALBUM_NAME] == "Album"
        assert result[AppMetadataKey.ALBUM_ARTISTS_NAMES] == ["C"]
        assert result[AppMetadataKey.GENRES_NAMES] == ["Rock"]
        assert result[AppMetadataKey.RATING] == 80
        assert result[AppMetadataKey.LANGUAGE] == "en"

    def test_rating_string_converted_to_int(self):
        result = build_app_metadata_from_payload({"rating": "50"})
        assert result[AppMetadataKey.RATING] == 50

    def test_rating_invalid_then_none(self):
        result = build_app_metadata_from_payload({"rating": "nope"})
        assert result[AppMetadataKey.RATING] is None

    def test_unknown_keys_ignored(self):
        result = build_app_metadata_from_payload({"title": "T", "other": "x"})
        assert AppMetadataKey.TITLE in result
        assert "other" not in result and len(result) == 1
