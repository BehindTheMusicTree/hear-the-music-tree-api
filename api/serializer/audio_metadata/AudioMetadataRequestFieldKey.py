from enum import Enum


class AudioMetadataRequestFieldKey(str, Enum):
    """Request keys for the full-metadata endpoint (non-tag fields)."""

    FILE = "file"
    INCLUDE_MUSICBRAINZ_ANALYSIS = "include_musicbrainz_analysis"
