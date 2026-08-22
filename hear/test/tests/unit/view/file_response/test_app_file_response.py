import os
import tempfile

from hear.view.file_response.AppFileResponse import AppFileResponse


class TestAppFileResponse:
    def test_filename_with_path_then_uses_basename_in_content_disposition(self):
        content_disposition = AppFileResponse._build_content_disposition("../../music/my track.mp3")
        assert 'filename="my track.mp3"' in content_disposition
        assert "music/" not in content_disposition
        assert "../" not in content_disposition

    def test_filename_with_windows_path_then_uses_basename_in_content_disposition(self):
        content_disposition = AppFileResponse._build_content_disposition("C:\\music\\my track.mp3")
        assert 'filename="my track.mp3"' in content_disposition
        assert "music" not in content_disposition
        assert "C:" not in content_disposition

    def test_filename_with_control_chars_then_removes_control_chars_in_content_disposition(self):
        content_disposition = AppFileResponse._build_content_disposition("my\r\ntrack.mp3")
        assert "\r" not in content_disposition
        assert "\n" not in content_disposition
        assert 'filename="mytrack.mp3"' in content_disposition

    def test_filename_with_non_ascii_then_sets_ascii_fallback_and_utf8_filename(self):
        content_disposition = AppFileResponse._build_content_disposition("café 🎵.mp3")
        assert 'filename="caf .mp3"' in content_disposition
        assert "filename*=UTF-8''caf%C3%A9%20%F0%9F%8E%B5.mp3" in content_disposition

    def test_empty_filename_then_uses_download_for_filename_and_filename_star(self):
        content_disposition = AppFileResponse._build_content_disposition("")
        assert 'filename="download"' in content_disposition
        assert "filename*=UTF-8''download" in content_disposition

    def test_filename_with_non_ascii_only_name_then_uses_download_fallback(self):
        content_disposition = AppFileResponse._build_content_disposition("🎵.mp3")
        assert 'filename="download.mp3"' in content_disposition
        assert "filename*=UTF-8''%F0%9F%8E%B5.mp3" in content_disposition

    def test_from_file_with_known_extension_then_sets_detected_content_type(self):
        with tempfile.NamedTemporaryFile(suffix=".mp3", delete=False) as tmp_file:
            tmp_file.write(b"content")
            file_path = tmp_file.name
        response = None
        try:
            response = AppFileResponse.from_file(file_path=file_path, filename="track.mp3")
            assert response.get("Content-Type") == "audio/mpeg"
        finally:
            if response is not None:
                response.close()
            if os.path.exists(file_path):
                os.unlink(file_path)

    def test_from_file_with_unknown_extension_then_sets_octet_stream_content_type(self):
        with tempfile.NamedTemporaryFile(suffix=".unknownext", delete=False) as tmp_file:
            tmp_file.write(b"content")
            file_path = tmp_file.name
        response = None
        try:
            response = AppFileResponse.from_file(file_path=file_path, filename="track.unknownext")
            assert response.get("Content-Type") == "application/octet-stream"
        finally:
            if response is not None:
                response.close()
            if os.path.exists(file_path):
                os.unlink(file_path)
