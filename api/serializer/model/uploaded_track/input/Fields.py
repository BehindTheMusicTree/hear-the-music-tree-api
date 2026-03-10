from api.model.uploaded_track.Fields import Fields as ModelFields
from api.utils.audio_file_metadata.AppMetadataKey import AppMetadataKey


class Fields:
    TRACK_FILE_INTERNAL = ModelFields.TRACK_FILE_INTERNAL
    TRACK_FILE_PUBLIC = ModelFields.TRACK_FILE_PUBLIC
    TRACK_FILE_FINGERPRINT_MUST_BE_UNIQUE = ModelFields.TRACK_FILE_FINGERPRINT_MUST_BE_UNIQUE
    TITLE = AppMetadataKey.TITLE
    FORCE_TITLE_GENERATION = "force_title_generation"
    ARTISTS_NAMES = AppMetadataKey.ARTISTS_NAMES
    ARTISTS_NAMES_MULTIPART = f"{ARTISTS_NAMES}[]"
    ALBUM_NAME = AppMetadataKey.ALBUM_NAME
    ALBUM_ARTISTS_NAMES = AppMetadataKey.ALBUM_ARTISTS_NAMES
    ALBUM_ARTISTS_NAMES_MULTIPART = f"{ALBUM_ARTISTS_NAMES}[]"
    TRACK_NUMBER = ModelFields.TRACK_NUMBER
    GENRE = ModelFields.GENRE
    RATING = AppMetadataKey.RATING
    LANGUAGE = AppMetadataKey.LANGUAGE
    ARCHIVED = ModelFields.ARCHIVED
