from enum import StrEnum


class UploadedTrackInputFieldKey(StrEnum):
    TRACK_FILE_INTERNAL = "track_file"
    TRACK_FILE_PUBLIC = "file"
    TRACK_FILE_FINGERPRINT_MUST_BE_UNIQUE = "track_file_fingerprint_must_be_unique"
    TITLE = "title"
    FORCE_TITLE_GENERATION = "force_title_generation"
    ARTISTS_NAMES = "artists_names"
    ARTISTS_NAMES_MULTIPART = "artists_names[]"
    ALBUM_NAME = "album_name"
    ALBUM_ARTISTS_NAMES = "album_artists_names"
    ALBUM_ARTISTS_NAMES_MULTIPART = "album_artists_names[]"
    TRACK_NUMBER = "track_number"
    GENRE = "genre"
    RATING = "rating"
    LANGUAGE = "language"
    ARCHIVED = "archived"
