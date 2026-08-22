from rest_framework import serializers


class AudioMetadataRequestUrlSerializer(serializers.Serializer):
    """
    OpenAPI schema only (application/json). Used in extend_schema so the docs
    show "URL in JSON body". The view validates with AudioMetadataFullSerializer.
    """

    file = serializers.URLField(required=True)
    include_musicbrainz_analysis = serializers.BooleanField(required=False, default=False)
