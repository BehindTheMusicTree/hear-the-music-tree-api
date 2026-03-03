from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import extend_schema
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView

from api.serializer.audio_metadata.AudioMetadataFull import AudioMetadataFullSerializer
from api.serializer.audio_metadata.AudioMetadataRequestFile import AudioMetadataRequestFileSerializer
from api.serializer.audio_metadata.AudioMetadataRequestUrl import AudioMetadataRequestUrlSerializer
from api.serializer.audio_metadata.Fields import Fields
from api.utils.audio_file_metadata import audiometa_adapter


class AudioMetadataView(APIView):

    @extend_schema(
        request={
            'multipart/form-data': AudioMetadataRequestFileSerializer,
            'application/json': AudioMetadataRequestUrlSerializer,
        },
        responses=OpenApiTypes.OBJECT,
        description='Accepts either an audio file (multipart) or a URL to an audio file (JSON).',
    )
    def post(self, request):
        serializer = AudioMetadataFullSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        file: audiometa_adapter.FILE_TYPE = serializer.validated_data.get(
            Fields.FILE)   # pyright: ignore[reportAssignmentType]
        full_metadata = audiometa_adapter.get_full_metadata(file, include_raw_binary_data=False)
        return Response(data=full_metadata, status=status.HTTP_200_OK)
