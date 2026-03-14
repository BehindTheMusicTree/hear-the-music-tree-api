from rest_framework import serializers

from api.serializer.field.TrackFileField import TrackFileField


class AudioMetadataFullSerializer(serializers.Serializer):
    """
    Runtime request validation. Accepts either uploaded file or URL (TrackFileField
    normalizes URL to a downloaded file). Used by AudioMetadataView.post; the
    RequestFile/RequestUrl serializers are for OpenAPI only.
    """
    file = TrackFileField(required=True)
    include_musicbrainz_analysis = serializers.BooleanField(
        required=False, default=False
    )
