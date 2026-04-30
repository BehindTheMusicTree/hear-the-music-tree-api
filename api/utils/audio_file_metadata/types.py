from enum import StrEnum

from .AppMetadataKey import AppMetadataKey


class RawMetadataKey(StrEnum):
    def __str__(self) -> str:
        return str(self.value)


"""
Raw metadata value can be none (when not set), string (title), integer (rating), float(BPM) or list[str] (artists
names).
"""
AppMetadataValue = int | float | str | list[str] | None
RawMetadataValue = list[int] | list[float] | list[str] | None
RawMetadataDict = dict[RawMetadataKey, RawMetadataValue]
AppMetadata = dict[AppMetadataKey, AppMetadataValue]
