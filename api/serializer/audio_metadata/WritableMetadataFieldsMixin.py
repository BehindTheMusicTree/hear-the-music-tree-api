"""DRF fields for writable file metadata (session download and uploaded track update)."""

from rest_framework import serializers


class WritableMetadataFieldsMixin(serializers.Serializer):
    """Mixin that declares the same metadata fields written to the audio file in both metadata-session
    download and uploaded track update_file_metadata. Add this to serializers that accept these fields.

    Field names follow ``UnifiedMetadataKey.value`` where applicable. Use ``artists_names``,
    ``album_name``, and ``album_artists_names`` for track artists, album title, and album
    artists; the metadata-session patch builder maps them to unified ``artists``, ``album``,
    and ``album_artists``.
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
    release_date = serializers.CharField(required=False, allow_blank=True)
    track_number = serializers.CharField(required=False, allow_blank=True)
    disc_number = serializers.IntegerField(required=False, allow_null=True)
    disc_total = serializers.IntegerField(required=False, allow_null=True)
    bpm = serializers.IntegerField(required=False, allow_null=True)
    composer = serializers.ListField(
        child=serializers.CharField(allow_blank=True),
        required=False,
        allow_empty=True,
    )
    publisher = serializers.CharField(required=False, allow_blank=True)
    copyright = serializers.CharField(required=False, allow_blank=True)
    unsynchronized_lyrics = serializers.CharField(required=False, allow_blank=True)
    comment = serializers.CharField(required=False, allow_blank=True)
    replaygain = serializers.CharField(required=False, allow_blank=True)
    archival_location = serializers.CharField(required=False, allow_blank=True)
    isrc = serializers.CharField(required=False, allow_blank=True)
    musicbrainz_trackid = serializers.CharField(required=False, allow_blank=True)
    musicbrainz_artistids = serializers.ListField(
        child=serializers.CharField(allow_blank=True),
        required=False,
        allow_empty=True,
    )
    description = serializers.CharField(required=False, allow_blank=True)
    originator = serializers.CharField(required=False, allow_blank=True)
