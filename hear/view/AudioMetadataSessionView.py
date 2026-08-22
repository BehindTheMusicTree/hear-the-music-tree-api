"""Create a metadata session: upload file, return metadata + session token (15 min TTL)."""

from django.core.files.uploadedfile import TemporaryUploadedFile
from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from hear.serializer.audio_metadata.AudioMetadataRequestFile import AudioMetadataRequestFileSerializer
from hear.serializer.audio_metadata.AudioMetadataRequestUrl import AudioMetadataRequestUrlSerializer
from hear.serializer.audio_metadata.Fields import Fields
from hear.utils import audio_fingerprinter, musicbrainz
from hear.utils.audio_file_metadata import audiometa_adapter
from hear.utils.audio_file_metadata.audiometa_adapter import FILE_TYPE
from hear.utils.file_path_utils import get_file_name_original, get_file_path
from hear.utils.metadata_session import create_session
from hear.utils.musicbrainz.service import (
    ANALYSIS_CODE,
    ANALYSIS_ERROR,
    ANALYSIS_MESSAGE,
)

MUSICBRAINZ_RAW_DATA = "musicbrainz_raw_data"
FINGERPRINT_FAILED_ERROR = "fingerprint_failed"


class AudioMetadataSessionView(APIView):
    """POST: upload file (or URL), get metadata + session_token. Session valid 15 min, multi-use for download."""

    @extend_schema(
        request={
            "multipart/form-data": AudioMetadataRequestFileSerializer,
            "application/json": AudioMetadataRequestUrlSerializer,
        },
        responses=OpenApiTypes.OBJECT,
        description=(
            "Upload an audio file (or URL). Returns metadata (same shape as /audio/metadata/full/) "
            "plus session_token and session_expires_in_seconds (900). Use the token in the download "
            "endpoint to get the file with updated metadata. Session is valid 15 minutes; you can "
            "download multiple times with different metadata."
        ),
    )
    def post(self, request):
        from hear.serializer.audio_metadata.AudioMetadataFull import AudioMetadataFullSerializer

        serializer = AudioMetadataFullSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        file: FILE_TYPE = serializer.validated_data.get(Fields.FILE)
        include_musicbrainz_analysis = serializer.validated_data.get(Fields.INCLUDE_MUSICBRAINZ_ANALYSIS, False)
        try:
            file_path = get_file_path(file)
            original_filename = get_file_name_original(file)
            full_metadata = audiometa_adapter.get_full_metadata(file, include_raw_binary_data=False)
            if include_musicbrainz_analysis:
                title = getattr(file, "name", "") or ""
                fp_result = audio_fingerprinter.service.get_fingerprint_and_duration_for_analysis(file, title=title)
                fingerprint = fp_result.get(audio_fingerprinter.service.RESULT_FINGERPRINT)
                if fingerprint is None:
                    full_metadata[MUSICBRAINZ_RAW_DATA] = {
                        ANALYSIS_ERROR: FINGERPRINT_FAILED_ERROR,
                        ANALYSIS_CODE: fp_result.get(audio_fingerprinter.service.RESULT_ERROR_CODE),
                        ANALYSIS_MESSAGE: fp_result.get(audio_fingerprinter.service.RESULT_ERROR_MESSAGE),
                    }
                else:
                    duration_sec = fp_result[audio_fingerprinter.service.RESULT_DURATION_IN_SEC]
                    mb_result = musicbrainz.service.get_musicbrainz_recording_analysis(
                        fingerprint=fingerprint, duration_in_sec=duration_sec
                    )
                    full_metadata[MUSICBRAINZ_RAW_DATA] = mb_result
            token, ttl = create_session(file_path, original_filename)
            full_metadata[Fields.SESSION_TOKEN] = token
            full_metadata[Fields.SESSION_EXPIRES_IN_SECONDS] = ttl
            return Response(data=full_metadata, status=status.HTTP_200_OK)
        finally:
            if isinstance(file, TemporaryUploadedFile):
                file.close()
