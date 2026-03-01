from rest_framework import serializers


class AudioMetadataRequestFileSerializer(serializers.Serializer):
    """Request body for POST when sending an audio file (multipart/form-data)."""

    file = serializers.FileField(required=True)
