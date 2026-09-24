from unittest.mock import MagicMock, Mock, patch

import pytest
from django.core.files.uploadedfile import SimpleUploadedFile
from the_music_tree_api_kit.exception.validation.app.AppValidationException import AppValidationException
from the_music_tree_api_kit.exception.validation.FieldValidationErrorCode import FieldValidationErrorCode

from hear.validator.TrackFileValidator import TrackFileValidator


class TestTrackFileValidator:
    def test_valid_mp3_extension_then_passes(self):
        validator = TrackFileValidator()
        file = SimpleUploadedFile("test.mp3", b"fake content", content_type="audio/mpeg")

        with (
            patch.object(validator, "_validate_file_size"),
            patch.object(validator, "_validate_content_type_is_audio_from_magic_bytes_and_content"),
        ):
            validator(file)

    def test_invalid_extension_then_raises_app_validation_exception(self):
        validator = TrackFileValidator()
        file = SimpleUploadedFile("test.txt", b"fake content", content_type="text/plain")

        with pytest.raises(AppValidationException) as exc_info:
            validator(file)

        assert exc_info.value.field_validation_error_code == FieldValidationErrorCode.TRACK_FILE_EXTENSION_INVALID

    def test_file_too_large_then_raises_app_validation_exception(self):
        from hear import settings

        validator = TrackFileValidator()
        max_size_bytes = settings.UPLOADED_TRACK_FILE_SIZE_MAX_IN_MO * 1000000
        large_content = b"x" * (max_size_bytes + 1)
        file = SimpleUploadedFile("test.mp3", large_content, content_type="audio/mpeg")

        with (
            patch.object(validator, "_validate_extension"),
            patch.object(validator, "_validate_content_type_is_audio_from_magic_bytes_and_content"),
        ):
            with pytest.raises(AppValidationException) as exc_info:
                validator(file)

            assert exc_info.value.field_validation_error_code == FieldValidationErrorCode.FILE_TOO_LARGE

    @patch("hear.validator.TrackFileValidator.settings")
    def test_file_too_small_then_raises_app_validation_exception(self, mock_settings):
        from hear import settings

        mock_settings.UPLOADED_TRACK_FILE_EXTENSIONS = settings.UPLOADED_TRACK_FILE_EXTENSIONS
        mock_settings.UPLOADED_TRACK_FILE_SIZE_MAX_IN_MO = settings.UPLOADED_TRACK_FILE_SIZE_MAX_IN_MO
        mock_settings.UPLOADED_TRACK_FILE_SIZE_MIN_IN_MO = 0.01
        validator = TrackFileValidator()
        min_size_bytes = int(mock_settings.UPLOADED_TRACK_FILE_SIZE_MIN_IN_MO * 1000000)
        tiny_content = b"x" * (min_size_bytes - 1)
        file = SimpleUploadedFile("test.mp3", tiny_content, content_type="audio/mpeg")

        with (
            patch.object(validator, "_validate_extension"),
            patch.object(validator, "_validate_content_type_is_audio_from_magic_bytes_and_content"),
        ):
            with pytest.raises(AppValidationException) as exc_info:
                validator(file)

            assert exc_info.value.field_validation_error_code == FieldValidationErrorCode.FILE_TOO_SMALL

    def test_id3_magic_bytes_then_passes(self):
        validator = TrackFileValidator()
        file = SimpleUploadedFile("test.mp3", b"ID3\x04\x00", content_type="audio/mpeg")
        file.size = 1024 * 1024

        with patch.object(validator, "_validate_extension"), patch.object(validator, "_validate_file_size"):
            validator(file)

    def test_riff_magic_bytes_then_passes(self):
        validator = TrackFileValidator()
        file = SimpleUploadedFile("test.wav", b"RIFF", content_type="audio/wav")
        file.size = 1024 * 1024

        with patch.object(validator, "_validate_extension"), patch.object(validator, "_validate_file_size"):
            validator(file)

    def test_flac_magic_bytes_then_passes(self):
        validator = TrackFileValidator()
        file = SimpleUploadedFile("test.flac", b"fLaC", content_type="audio/flac")
        file.size = 1024 * 1024

        with patch.object(validator, "_validate_extension"), patch.object(validator, "_validate_file_size"):
            validator(file)

    @patch("hear.validator.TrackFileValidator.audiometa.get_unified_metadata")
    @patch("hear.validator.TrackFileValidator.get_file_path")
    def test_valid_audio_file_then_passes(self, mock_get_path, mock_get_metadata):
        validator = TrackFileValidator()
        file = SimpleUploadedFile("test.mp3", b"fake content", content_type="audio/mpeg")
        file.size = 1024 * 1024
        mock_get_path.return_value = "/path/to/file.mp3"
        mock_get_metadata.return_value = {}

        with patch.object(validator, "_validate_extension"), patch.object(validator, "_validate_file_size"):
            validator(file)

        mock_get_metadata.assert_called_once()

    @patch("hear.validator.TrackFileValidator.audiometa.get_unified_metadata")
    @patch("hear.validator.TrackFileValidator.get_file_path")
    def test_invalid_audio_file_then_raises_app_validation_exception(self, mock_get_path, mock_get_metadata):
        validator = TrackFileValidator()
        file = SimpleUploadedFile("test.mp3", b"fake content", content_type="audio/mpeg")
        file.size = 1024 * 1024
        mock_get_path.return_value = "/path/to/file.mp3"
        mock_get_metadata.side_effect = Exception("Not an audio file")

        with patch.object(validator, "_validate_extension"), patch.object(validator, "_validate_file_size"):
            with pytest.raises(AppValidationException) as exc_info:
                validator(file)

            assert exc_info.value.field_validation_error_code == FieldValidationErrorCode.TRACK_FILE_TYPE_INVALID
