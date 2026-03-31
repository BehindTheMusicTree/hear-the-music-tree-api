import os
from mimetypes import guess_type
from urllib.parse import quote

from django.http import FileResponse

from api.view.error.ApiErrorCode import ApiErrorCodeNumeric
from api.view.error.ErrorResponseFields import ErrorResponseFields
from api.view.file_response.FileResponseHeaders import FileResponseHeaders


class AppFileResponse:
    @staticmethod
    def from_file(file_path: str, filename: str) -> FileResponse:
        if not os.path.exists(file_path):
            raise FileNotFoundError(ErrorResponseFields.MESSAGES[ApiErrorCodeNumeric.RESOURCE_FILE_NOT_FOUND])

        file_handle = open(file_path, "rb")
        guessed_content_type, _ = guess_type(filename or file_path)
        content_type = guessed_content_type or FileResponseHeaders.CONTENT_TYPE_DEFAULT
        response = FileResponse(file_handle, content_type=content_type)
        response[FileResponseHeaders.CONTENT_LENGTH] = os.path.getsize(file_path)
        response[FileResponseHeaders.CONTENT_DISPOSITION] = AppFileResponse._build_content_disposition(filename)
        response[FileResponseHeaders.ACCESS_CONTROL_EXPOSE_HEADERS] = (
            FileResponseHeaders.ACCESS_CONTROL_EXPOSE_HEADERS_CONTENT_DISPOSITION_VALUE
        )
        return response

    @staticmethod
    def _build_content_disposition(filename: str) -> str:
        effective_filename = AppFileResponse._build_effective_filename(filename)
        fallback_filename = AppFileResponse._build_ascii_fallback_filename(effective_filename)
        encoded_filename = quote(effective_filename, safe="")
        return (
            f'attachment; filename="{fallback_filename}"; '
            f"filename*=UTF-8''{encoded_filename}"
        )

    @staticmethod
    def _build_ascii_fallback_filename(filename: str) -> str:
        if not filename:
            return "download"
        _, extension = os.path.splitext(filename)
        fallback = filename.encode("ascii", "ignore").decode("ascii")
        fallback = fallback.replace('"', "").replace("\\", "").strip()
        fallback_stem = fallback[: -len(extension)] if extension and fallback.endswith(extension) else fallback
        if fallback and fallback_stem.strip():
            return fallback
        return f"download{extension}" if extension else "download"

    @staticmethod
    def _build_effective_filename(filename: str) -> str:
        normalized = (filename or "").replace("\\", "/")
        basename = os.path.basename(normalized)
        sanitized_chars = []
        for char in basename:
            char_code = ord(char)
            if char_code < 32 or char_code == 127:
                continue
            sanitized_chars.append(char)
        sanitized_filename = "".join(sanitized_chars).strip()
        return sanitized_filename or "download"
