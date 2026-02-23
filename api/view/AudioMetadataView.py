from rest_framework.views import APIView

from api.serializer.audio_metadata.AudioMetadataFull import AudioMetadataFullSerializer


class AudioMetadataView(APIView):

    def post(self, request):
        serializer = AudioMetadataFullSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
