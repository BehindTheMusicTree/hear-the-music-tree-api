from rest_framework import serializers


class AudioMetadataRequestUrlSerializer(serializers.Serializer):
    """Request body for POST when sending an audio file URL (application/json)."""

    file = serializers.URLField(required=True)
