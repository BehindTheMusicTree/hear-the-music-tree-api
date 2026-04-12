from unittest.mock import patch

import pytest

from api.utils.audio_file_metadata import (
    AppMetadataKey,
    delete_metadata,
    get_app_metadata,
    get_bitrate,
    get_duration_in_sec,
    get_specific_metadata,
    is_flac_md5_valid,
    update_file_metadata,
)
from api.utils.audio_file_metadata.audiometa_adapter import (
    _APP_TO_UNIFIED_KEY_MAP,
    AudiometaFileCorruptedError,  # type: ignore[attr-defined]
    UnifiedMetadataKey,  # type: ignore[attr-defined]
    delete_potential_id3_metadata_with_header,
)
from api.utils.audio_file_metadata.audiometa_adapter import (
    MetadataFormat as AudiometaMetadataFormat,
)
from api.utils.audio_file_metadata.exceptions import FileCorruptedError

ADAPTER_MODULE = "api.utils.audio_file_metadata.audiometa_adapter"


class TestGetMergedAppMetadata:
    @patch(ADAPTER_MODULE + ".audiometa.get_unified_metadata")
    @patch(ADAPTER_MODULE + "._get_file_path_util")
    def test_valid_file_then_returns_app_metadata(self, mock_get_path, mock_get_unified):
        mock_get_path.return_value = "/path/to/file.mp3"
        mock_get_unified.return_value = {
            UnifiedMetadataKey.TITLE: "Test Title",
            UnifiedMetadataKey.ARTISTS: ["Artist 1", "Artist 2"],
            UnifiedMetadataKey.RATING: 85,
        }

        result = get_app_metadata("/path/to/file.mp3", normalized_rating_max_value=100)

        assert result[AppMetadataKey.TITLE] == "Test Title"
        assert result[AppMetadataKey.ARTISTS_NAMES] == ["Artist 1", "Artist 2"]
        assert result[AppMetadataKey.RATING] == 85
        mock_get_unified.assert_called_once_with(file="/path/to/file.mp3", normalized_rating_max_value=100)

    @patch(ADAPTER_MODULE + ".audiometa.get_unified_metadata")
    @patch(ADAPTER_MODULE + "._get_file_path_util")
    def test_corrupted_file_then_raises_file_corrupted_error(self, mock_get_path, mock_get_unified):
        mock_get_path.return_value = "/path/to/corrupted.mp3"
        mock_get_unified.side_effect = AudiometaFileCorruptedError("File is corrupted")

        with pytest.raises(FileCorruptedError, match="File is corrupted"):
            get_app_metadata("/path/to/corrupted.mp3")

    @patch(ADAPTER_MODULE + ".audiometa.get_unified_metadata")
    @patch(ADAPTER_MODULE + "._get_file_path_util")
    def test_genres_names_list_then_passed_through(self, mock_get_path, mock_get_unified):
        mock_get_path.return_value = "/path/to/file.mp3"
        mock_get_unified.return_value = {
            UnifiedMetadataKey.GENRES_NAMES: ["Rock", "Metal"],
        }

        result = get_app_metadata("/path/to/file.mp3")

        assert result[AppMetadataKey.GENRES_NAMES] == ["Rock", "Metal"]


class TestGetSpecificMetadata:
    @patch(ADAPTER_MODULE + ".audiometa.get_unified_metadata_field")
    @patch(ADAPTER_MODULE + "._get_file_path_util")
    def test_title_then_returns_title(self, mock_get_path, mock_get_field):
        mock_get_path.return_value = "/path/to/file.mp3"
        mock_get_field.return_value = "Test Title"

        result = get_specific_metadata("/path/to/file.mp3", AppMetadataKey.TITLE)

        assert result == "Test Title"
        mock_get_field.assert_called_once_with(file="/path/to/file.mp3", unified_metadata_key=UnifiedMetadataKey.TITLE)

    @patch(ADAPTER_MODULE + ".audiometa.get_unified_metadata_field")
    @patch(ADAPTER_MODULE + "._get_file_path_util")
    def test_genres_names_then_returns_list(self, mock_get_path, mock_get_field):
        mock_get_path.return_value = "/path/to/file.mp3"
        mock_get_field.return_value = ["Rock", "Metal"]

        result = get_specific_metadata("/path/to/file.mp3", AppMetadataKey.GENRES_NAMES)

        assert result == ["Rock", "Metal"]

    @patch(ADAPTER_MODULE + ".audiometa.get_unified_metadata_field")
    @patch(ADAPTER_MODULE + "._get_file_path_util")
    def test_unknown_key_then_returns_none(self, mock_get_path, mock_get_field):
        mock_get_path.return_value = "/path/to/file.mp3"

        unknown_key = None
        for key in AppMetadataKey:
            if key not in _APP_TO_UNIFIED_KEY_MAP:
                unknown_key = key
                break

        if unknown_key is None:
            pytest.skip("All AppMetadataKey values are mapped, cannot test unknown key")

        result = get_specific_metadata("/path/to/file.mp3", unknown_key)

        assert result is None
        mock_get_field.assert_not_called()


class TestUpdateFileMetadata:
    @patch(ADAPTER_MODULE + ".audiometa.update_metadata")
    @patch(ADAPTER_MODULE + "._get_file_path_util")
    def test_update_metadata_then_calls_audiometa(self, mock_get_path, mock_update):
        mock_get_path.return_value = "/path/to/file.mp3"
        app_metadata = {
            AppMetadataKey.TITLE: "New Title",
            AppMetadataKey.RATING: 85,
        }

        update_file_metadata("/path/to/file.mp3", app_metadata, normalized_rating_max_value=100)

        mock_update.assert_called_once()
        call_args = mock_update.call_args
        assert call_args.kwargs["file"] == "/path/to/file.mp3"
        assert call_args.kwargs["normalized_rating_max_value"] == 100
        assert UnifiedMetadataKey.TITLE in call_args.kwargs["unified_metadata"]
        assert call_args.kwargs["unified_metadata"][UnifiedMetadataKey.TITLE] == "New Title"


class TestDeleteMetadata:
    @patch(ADAPTER_MODULE + ".audiometa.delete_all_metadata")
    @patch(ADAPTER_MODULE + "._get_file_path_util")
    def test_delete_all_metadata_then_calls_audiometa(self, mock_get_path, mock_delete):
        mock_get_path.return_value = "/path/to/file.mp3"
        mock_delete.return_value = True

        result = delete_metadata("/path/to/file.mp3")

        assert result is True
        mock_delete.assert_called_once_with(file="/path/to/file.mp3", metadata_format=None)


class TestGetBitrate:
    @patch(ADAPTER_MODULE + ".audiometa.get_bitrate")
    @patch(ADAPTER_MODULE + "._get_file_path_util")
    def test_get_bitrate_then_returns_kbps(self, mock_get_path, mock_get_bitrate):
        mock_get_path.return_value = "/path/to/file.mp3"
        mock_get_bitrate.return_value = 320000

        result = get_bitrate("/path/to/file.mp3")

        assert result == 320
        mock_get_bitrate.assert_called_once_with(file="/path/to/file.mp3")


class TestGetDurationInSec:
    @patch(ADAPTER_MODULE + ".audiometa.get_duration_in_sec")
    @patch(ADAPTER_MODULE + "._get_file_path_util")
    def test_get_duration_then_returns_duration(self, mock_get_path, mock_get_duration):
        mock_get_path.return_value = "/path/to/file.mp3"
        mock_get_duration.return_value = 180.5

        result = get_duration_in_sec("/path/to/file.mp3")

        assert result == 180.5
        mock_get_duration.assert_called_once_with(file="/path/to/file.mp3")


class TestIsFlacMd5Valid:
    @patch(ADAPTER_MODULE + ".audiometa.is_flac_md5_valid")
    @patch(ADAPTER_MODULE + "._get_file_path_util")
    def test_valid_md5_then_returns_true(self, mock_get_path, mock_is_valid):
        mock_get_path.return_value = "/path/to/file.flac"
        mock_is_valid.return_value = True

        result = is_flac_md5_valid("/path/to/file.flac")

        assert result is True
        mock_is_valid.assert_called_once_with(file="/path/to/file.flac")

    @patch(ADAPTER_MODULE + ".audiometa.is_flac_md5_valid")
    @patch(ADAPTER_MODULE + "._get_file_path_util")
    def test_invalid_md5_then_returns_false(self, mock_get_path, mock_is_valid):
        mock_get_path.return_value = "/path/to/file.flac"
        mock_is_valid.return_value = False

        result = is_flac_md5_valid("/path/to/file.flac")

        assert result is False


class TestDeletePotentialId3MetadataWithHeader:
    @patch(ADAPTER_MODULE + ".audiometa.delete_all_metadata")
    @patch(ADAPTER_MODULE + "._get_file_path_util")
    def test_id3_present_then_deletes(self, mock_get_path, mock_delete):
        mock_get_path.return_value = "/path/to/file.flac"
        mock_delete.return_value = True

        delete_potential_id3_metadata_with_header("/path/to/file.flac")

        mock_delete.assert_called_once_with(file="/path/to/file.flac", metadata_format=AudiometaMetadataFormat.ID3V2)

    @patch(ADAPTER_MODULE + ".audiometa.delete_all_metadata")
    @patch(ADAPTER_MODULE + "._get_file_path_util")
    def test_id3_not_present_then_silently_passes(self, mock_get_path, mock_delete):
        mock_get_path.return_value = "/path/to/file.flac"
        mock_delete.side_effect = Exception("No ID3 tags")

        delete_potential_id3_metadata_with_header("/path/to/file.flac")

        mock_delete.assert_called_once()
