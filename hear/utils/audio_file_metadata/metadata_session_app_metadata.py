"""Build AppMetadata from a request payload (e.g. metadata-session download metadata body)."""

from hear.utils.audio_file_metadata.AppMetadataKey import (
    APP_METADATA_WRITABLE_KEYS,
    AppMetadataKey,
)
from hear.utils.audio_file_metadata.types import AppMetadata

PAYLOAD_KEY_TO_APP_KEY = {k.value: k for k in APP_METADATA_WRITABLE_KEYS}


def build_app_metadata_from_payload(payload: dict) -> AppMetadata:
    """Build AppMetadata from a dict with keys title, artists_names, album_name, etc.

    Only keys present in payload are included. Use None or empty list/string to clear a tag.
    Uses the same writable metadata keys as uploaded track file metadata updates.
    """
    app_metadata: AppMetadata = {}
    for payload_key, app_key in PAYLOAD_KEY_TO_APP_KEY.items():
        if payload_key not in payload:
            continue
        value = payload[payload_key]
        if app_key == AppMetadataKey.RATING and value is not None:
            try:
                value = int(value)
            except TypeError, ValueError:
                value = None
        app_metadata[app_key] = value
    return app_metadata
