from rest_framework import serializers


class AudioMetadataRequestFileSerializer(serializers.Serializer):
    """
    OpenAPI schema only (multipart/form-data). Used in extend_schema so the docs
    show "file upload". The view validates with AudioMetadataFullSerializer.
    """

    file = serializers.FileField(required=True)
    include_musicbrainz_analysis = serializers.BooleanField(required=False, default=False)
