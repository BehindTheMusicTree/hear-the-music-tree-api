"""Build AppMetadata from a request payload (e.g. metadata-session download metadata body)."""

from audiometa import UnifiedMetadataKey

from api.utils.audio_file_metadata.AppMetadataKey import AppMetadataKey
from api.utils.audio_file_metadata.types import AppMetadata

PAYLOAD_KEY_TO_APP_KEY: dict[str, AppMetadataKey] = {
    AppMetadataKey.TITLE.value: AppMetadataKey.TITLE,
    UnifiedMetadataKey.ARTISTS.value: AppMetadataKey.ARTISTS_NAMES,
    UnifiedMetadataKey.ALBUM.value: AppMetadataKey.ALBUM_NAME,
    UnifiedMetadataKey.ALBUM_ARTISTS.value: AppMetadataKey.ALBUM_ARTISTS_NAMES,
    AppMetadataKey.GENRES_NAMES.value: AppMetadataKey.GENRES_NAMES,
    AppMetadataKey.RATING.value: AppMetadataKey.RATING,
    AppMetadataKey.LANGUAGE.value: AppMetadataKey.LANGUAGE,
}


def build_app_metadata_from_payload(payload: dict) -> AppMetadata:
    """Build AppMetadata from a dict keyed by unified metadata field ids (``UnifiedMetadataKey.value``).

    Only keys present in payload are included. Use None or empty list/string to clear a tag.
    """
    app_metadata: AppMetadata = {}
    for payload_key, app_key in PAYLOAD_KEY_TO_APP_KEY.items():
        if payload_key not in payload:
            continue
        value = payload[payload_key]
        if app_key == AppMetadataKey.RATING and value is not None:
            try:
                value = int(value)
            except (TypeError, ValueError):
                value = None
        app_metadata[app_key] = value
    return app_metadata
