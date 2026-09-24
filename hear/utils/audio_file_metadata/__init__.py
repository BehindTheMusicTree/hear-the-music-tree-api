"""Audio file metadata handling module."""

from .AppMetadataKey import APP_METADATA_WRITABLE_KEYS, AppMetadataKey
from .audiometa_adapter import (
    delete_metadata,
    fix_md5_checking,
    get_app_metadata,
    get_bitrate,
    get_duration_in_sec,
    get_full_metadata,
    get_specific_metadata,
    is_flac_md5_valid,
    update_file_metadata,
)
from .exceptions import FileCorruptedError
from .types import AppMetadata, AppMetadataValue

__all__ = [
    "APP_METADATA_WRITABLE_KEYS",
    "AppMetadata",
    "AppMetadataKey",
    "AppMetadataValue",
    "FileCorruptedError",
    "delete_metadata",
    "fix_md5_checking",
    "get_app_metadata",
    "get_bitrate",
    "get_duration_in_sec",
    "get_full_metadata",
    "get_specific_metadata",
    "is_flac_md5_valid",
    "update_file_metadata",
]
