"""Request body for metadata-session download: session token + metadata fields to write."""

from rest_framework import serializers

from api.serializer.audio_metadata.WritableMetadataFieldsMixin import WritableMetadataFieldsMixin


class AudioMetadataSessionDownloadSerializer(WritableMetadataFieldsMixin):
    """Validates session token and optional metadata fields for the download endpoint.

    Metadata fields (title, artists_names, etc.) are shared with uploaded track file metadata updates.
    """

    session_token = serializers.CharField(required=False, allow_blank=False)
