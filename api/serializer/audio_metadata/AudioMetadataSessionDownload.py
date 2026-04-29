from rest_framework import serializers

from api.serializer.audio_metadata.Fields import Fields


class AudioMetadataSessionDownloadSerializer(serializers.Serializer):
    """Optional JSON body for metadata-session download; token may also come from X-Session-Token."""

    session_token = serializers.CharField(required=False, allow_blank=True)
    title = serializers.CharField(required=False, allow_blank=True)
    artists_names = serializers.ListField(child=serializers.CharField(), required=False)
    album_name = serializers.CharField(required=False, allow_blank=True)
    album_artists_names = serializers.ListField(child=serializers.CharField(), required=False)
    genres_names = serializers.ListField(child=serializers.CharField(), required=False)
    rating = serializers.IntegerField(required=False, allow_null=True)
    language = serializers.CharField(required=False, allow_blank=True)
