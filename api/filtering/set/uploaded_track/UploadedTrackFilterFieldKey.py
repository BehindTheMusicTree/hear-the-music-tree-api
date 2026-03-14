from enum import Enum


class UploadedTrackFilterFieldKey(str, Enum):
    TITLE = "title"
    ARTISTS_NAME = "artists_name"
    ALBUM_NAME = "album_name"
    GENRE_NAME = "genre_name"
    LANGUAGE = "language"
