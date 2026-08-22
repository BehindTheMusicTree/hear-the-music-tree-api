from unittest.mock import patch

from django.core.files.uploadedfile import SimpleUploadedFile

from hear.utils.audio_fingerprinter.service import (
    RESULT_DURATION_IN_SEC,
    RESULT_ERROR_CODE,
    RESULT_ERROR_MESSAGE,
    RESULT_FINGERPRINT,
    get_fingerprint_and_duration_for_analysis,
)
from hear.utils.audio_fingerprinter.utils import exception as audio_fingerprinter_exc


class TestGetFingerprintAndDurationForAnalysisSuccess:
    def test_post_fingerprint_returns_data_then_dict_with_fingerprint_and_duration(self):
        file = SimpleUploadedFile("test.mp3", b"fake", content_type="audio/mpeg")
        with (
            patch(
                "hear.utils.file_path_utils.get_file_name_system",
                return_value="/tmp/test.mp3",
            ),
            patch(
                "hear.utils.audio_fingerprinter.utils.post_fingerprint_audio",
                return_value=(b"\x00" * 20, 120.5),
            ),
        ):
            result = get_fingerprint_and_duration_for_analysis(file, title="Test")
        assert result[RESULT_FINGERPRINT] == b"\x00" * 20
        assert result[RESULT_DURATION_IN_SEC] == 120.5
        assert result[RESULT_ERROR_CODE] is None
        assert result[RESULT_ERROR_MESSAGE] is None


class TestGetFingerprintAndDurationForAnalysisFailure:
    def test_post_fingerprint_raises_then_dict_with_error_code_and_message(self):
        file = SimpleUploadedFile("test.mp3", b"fake", content_type="audio/mpeg")
        with (
            patch(
                "hear.utils.file_path_utils.get_file_name_system",
                return_value="/tmp/test.mp3",
            ),
            patch(
                "hear.utils.audio_fingerprinter.utils.post_fingerprint_audio",
                side_effect=audio_fingerprinter_exc.TimeoutException("Timed out"),
            ),
        ):
            result = get_fingerprint_and_duration_for_analysis(file, title="")
        assert result[RESULT_FINGERPRINT] is None
        assert result[RESULT_DURATION_IN_SEC] is None
        assert result[RESULT_ERROR_CODE] == "timeout_error"
        assert result[RESULT_ERROR_MESSAGE] == "Timed out"

    def test_post_fingerprint_raises_wrong_file_extension_then_mapped_error_code(self):
        file = SimpleUploadedFile("test.mp3", b"fake", content_type="audio/mpeg")
        with (
            patch(
                "hear.utils.file_path_utils.get_file_name_system",
                return_value="/tmp/test.mp3",
            ),
            patch(
                "hear.utils.audio_fingerprinter.utils.post_fingerprint_audio",
                side_effect=audio_fingerprinter_exc.WrongFileExtension("Bad ext"),
            ),
        ):
            result = get_fingerprint_and_duration_for_analysis(file, title="")
        assert result[RESULT_FINGERPRINT] is None
        assert result[RESULT_ERROR_CODE] == "wrong_file_extension"
        assert result[RESULT_ERROR_MESSAGE] == "Bad ext"
