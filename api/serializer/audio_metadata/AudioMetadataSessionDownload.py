"""Request body for metadata-session download: session token + metadata fields to write."""

from rest_framework import serializers

from api.serializer.audio_metadata.WritableMetadataFieldsMixin import WritableMetadataFieldsMixin


class AudioMetadataSessionDownloadSerializer(WritableMetadataFieldsMixin):
    """Validates session token and optional metadata fields for the download endpoint.

    Metadata keys match unified field ids (``UnifiedMetadataKey.value``), e.g. ``artists``, ``album``.
    """

    session_token = serializers.CharField(required=False, allow_blank=False)
