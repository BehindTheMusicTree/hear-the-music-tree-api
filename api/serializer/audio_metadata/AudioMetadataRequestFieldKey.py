from enum import Enum


class AudioMetadataRequestFieldKey(str, Enum):
    """Request / response keys for audio metadata session and full-metadata endpoints (non-tag fields)."""

    FILE = "file"
    INCLUDE_MUSICBRAINZ_ANALYSIS = "include_musicbrainz_analysis"
    SESSION_TOKEN = "session_token"
    SESSION_EXPIRES_IN_SECONDS = "session_expires_in_seconds"
