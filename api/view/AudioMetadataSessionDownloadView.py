"""Download file with updated metadata using a metadata-session token (multi-use until 15 min expiry)."""

import os
import shutil
import tempfile
from pathlib import Path

from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from api.serializer.audio_metadata.Fields import Fields
from api.utils.audio_file_metadata import audiometa_adapter
from api.utils.audio_file_metadata.metadata_session_app_metadata import build_app_metadata_from_payload
from api.utils.metadata_session import get_session
from api.view.file_response.AppFileResponse import AppFileResponse

NORMALIZED_RATING_MAX = 100
SESSION_TOKEN_HEADER = "X-Session-Token"


class AudioMetadataSessionDownloadView(APIView):
    """POST: send session_token (header or body) + optional metadata; returns file with tags written. Multi-use."""

    @extend_schema(
        request={"application/json": {"type": "object", "properties": {
            "session_token": {"type": "string"},
            "title": {"type": "string"},
            "artists_names": {"type": "array", "items": {"type": "string"}},
            "album_name": {"type": "string"},
            "album_artists_names": {"type": "array", "items": {"type": "string"}},
            "genres_names": {"type": "array", "items": {"type": "string"}},
            "rating": {"type": "integer"},
            "language": {"type": "string"},
        }}},
        responses={200: OpenApiTypes.BINARY, 404: None, 410: None},
        description=(
            "Download the file for the given session token with optional metadata written in. "
            "Send session_token in X-Session-Token header or in JSON body. Metadata fields are optional; "
            "only provided fields are written. Session is valid 15 minutes; you can call this multiple times "
            "with different metadata. Returns 404/410 if token is missing or expired. "
            "On success, the response sets Content-Type from the file, Content-Disposition with attachment "
            "and both filename (ASCII fallback) and filename* (RFC 5987 UTF-8), and "
            "Access-Control-Expose-Headers: Content-Disposition for cross-origin clients."
        ),
    )
    def post(self, request):
        from api.serializer.audio_metadata.AudioMetadataSessionDownload import (
            AudioMetadataSessionDownloadSerializer,
        )

        token = request.headers.get(SESSION_TOKEN_HEADER) or (request.data.get(Fields.SESSION_TOKEN) if request.data else None)
        if not token or not str(token).strip():
            return Response(
                {"detail": "Missing session token. Send X-Session-Token header or session_token in body."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        serializer = AudioMetadataSessionDownloadSerializer(data=request.data or {})
        serializer.is_valid(raise_exception=True)
        session = get_session(str(token).strip())
        if session is None:
            return Response(
                {"detail": "Session not found or expired. Upload again to get a new session."},
                status=status.HTTP_410_GONE,
            )
        stored_path, original_filename = session
        payload = serializer.validated_data.copy()
        payload.pop(Fields.SESSION_TOKEN, None)
        app_metadata = build_app_metadata_from_payload(payload)
        if not app_metadata:
            working_path = stored_path
        else:
            suffix = Path(stored_path).suffix or ".bin"
            fd, working_path = tempfile.mkstemp(suffix=suffix)
            os.close(fd)
            try:
                shutil.copy2(stored_path, working_path)
                audiometa_adapter.update_file_metadata(
                    working_path,
                    app_metadata,
                    normalized_rating_max_value=NORMALIZED_RATING_MAX,
                )
            except Exception:
                if os.path.exists(working_path):
                    try:
                        os.unlink(working_path)
                    except OSError:
                        pass
                raise
        try:
            return AppFileResponse.from_file(working_path, original_filename)
        finally:
            if working_path != stored_path and os.path.exists(working_path):
                try:
                    os.unlink(working_path)
                except OSError:
                    pass
