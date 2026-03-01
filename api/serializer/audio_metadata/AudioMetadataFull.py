from rest_framework.serializers import Serializer

from api.serializer.field.TrackFileField import TrackFileField


class AudioMetadataFullSerializer(Serializer):
    file = TrackFileField(required=True)
