from rest_framework import serializers

from api.serializer.field.TrackFileField import TrackFileField


class AudioMetadataFullSerializer(serializers.Serializer):
    file = TrackFileField(required=True)
    include_musicbrainz_analysis = serializers.BooleanField(
        required=False, default=False
    )
