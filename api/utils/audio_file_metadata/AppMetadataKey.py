"""Canonical keys for app-level file metadata (read/write tags, metadata API)."""

from enum import Enum

from django.core.exceptions import ImproperlyConfigured


class AppMetadataKey(str, Enum):
    """Keys used in AppMetadata dicts and metadata API payloads. Defined here as single source of truth."""

    TITLE = "title"
    ARTISTS_NAMES = "artists_names"
    ALBUM_NAME = "album_name"
    ALBUM_ARTISTS_NAMES = "album_artists_names"
    GENRES_NAMES = "genres_names"
    RATING = "rating"
    LANGUAGE = "language"

    def may_contain_separated_values(self) -> bool:
        result = self in (AppMetadataKey.ARTISTS_NAMES, AppMetadataKey.ALBUM_ARTISTS_NAMES)
        if result and self.get_optional_type() != list[str]:
            raise ImproperlyConfigured(f'Optional type for {self} is not list')
        return result

    def get_optional_type(self) -> type:
        APP_METADATA_KEYS_OPTIONAL_TYPES_MAP = {
            AppMetadataKey.TITLE: str,
            AppMetadataKey.ARTISTS_NAMES: list[str],
            AppMetadataKey.ALBUM_NAME: str,
            AppMetadataKey.ALBUM_ARTISTS_NAMES: list[str],
            AppMetadataKey.GENRES_NAMES: list[str],
            AppMetadataKey.RATING: int,
            AppMetadataKey.LANGUAGE: str,
        }
        type = APP_METADATA_KEYS_OPTIONAL_TYPES_MAP.get(self)
        if not type:
            raise ImproperlyConfigured(f'No optional type defined for {self}')
        return type


APP_METADATA_WRITABLE_KEYS: tuple[AppMetadataKey, ...] = (
    AppMetadataKey.TITLE,
    AppMetadataKey.ARTISTS_NAMES,
    AppMetadataKey.ALBUM_NAME,
    AppMetadataKey.ALBUM_ARTISTS_NAMES,
    AppMetadataKey.GENRES_NAMES,
    AppMetadataKey.RATING,
    AppMetadataKey.LANGUAGE,
)
