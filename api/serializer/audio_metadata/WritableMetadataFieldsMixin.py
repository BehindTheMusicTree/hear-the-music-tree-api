"""DRF fields for writable file metadata (session download and uploaded track update)."""

from rest_framework import serializers


class WritableMetadataFieldsMixin(serializers.Serializer):
    """Mixin that declares the same metadata fields written to the audio file in both metadata-session
    download and uploaded track update_file_metadata. Add this to serializers that accept these fields.
    """

    title = serializers.CharField(required=False, allow_blank=True)
    artists_names = serializers.ListField(
        child=serializers.CharField(allow_blank=True),
        required=False,
        allow_empty=True,
    )
    album_name = serializers.CharField(required=False, allow_blank=True)
    album_artists_names = serializers.ListField(
        child=serializers.CharField(allow_blank=True),
        required=False,
        allow_empty=True,
    )
    genres_names = serializers.ListField(
        child=serializers.CharField(allow_blank=True),
        required=False,
        allow_empty=True,
    )
    rating = serializers.IntegerField(required=False, allow_null=True, min_value=0)
    language = serializers.CharField(required=False, allow_blank=True)
