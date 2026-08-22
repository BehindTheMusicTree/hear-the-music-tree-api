from enum import StrEnum


class UploadedTrackOutputFieldKey(StrEnum):
    CREATED_ON = "created_on"
    UPDATED_ON = "updated_on"
    UUID = "uuid"
    RELATIVE_URL = "relative_url"
    FILE = "file"
    TITLE = "title"
    ARTISTS = "artists"
    ALBUM = "album"
    TRACK_NUMBER = "track_number"
    GENRE = "genre"
    RATING = "rating"
    LANGUAGE = "language"
    PLAYLISTS_PUBLIC = "playlists"
    PLAY_COUNT = "play_count"
    ARCHIVED = "archived"
