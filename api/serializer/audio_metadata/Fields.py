from enum import StrEnum

from audiometa import UnifiedMetadataKey

from api.serializer.audio_metadata.AudioMetadataRequestFieldKey import AudioMetadataRequestFieldKey
from api.utils.audio_file_metadata.AppMetadataKey import AppMetadataKey


class Fields(StrEnum):
    FILE = AudioMetadataRequestFieldKey.FILE.value
    INCLUDE_MUSICBRAINZ_ANALYSIS = AudioMetadataRequestFieldKey.INCLUDE_MUSICBRAINZ_ANALYSIS.value
    SESSION_TOKEN = AudioMetadataRequestFieldKey.SESSION_TOKEN.value
    SESSION_EXPIRES_IN_SECONDS = AudioMetadataRequestFieldKey.SESSION_EXPIRES_IN_SECONDS.value
    TITLE = AppMetadataKey.TITLE.value
    ARTISTS = UnifiedMetadataKey.ARTISTS.value
    ALBUM = UnifiedMetadataKey.ALBUM.value
    ALBUM_ARTISTS = UnifiedMetadataKey.ALBUM_ARTISTS.value
    ARTISTS_NAMES = AppMetadataKey.ARTISTS_NAMES.value
    ALBUM_NAME = AppMetadataKey.ALBUM_NAME.value
    ALBUM_ARTISTS_NAMES = AppMetadataKey.ALBUM_ARTISTS_NAMES.value
    GENRES_NAMES = AppMetadataKey.GENRES_NAMES.value
    RATING = AppMetadataKey.RATING.value
    LANGUAGE = AppMetadataKey.LANGUAGE.value
