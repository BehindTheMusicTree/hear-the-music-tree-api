from enum import StrEnum

from the_music_tree_genre_kit.serializer.model.criteria.output.CriteriaOutputFieldKey import (
    CriteriaOutputFieldKey as KitCriteriaOutputFieldKey,
)

# `StrEnum` can't be subclassed once it has members, so hear's extension of the kit's base
# enum is built via the functional API instead of plain class inheritance.
CriteriaOutputFieldKey = StrEnum(
    "CriteriaOutputFieldKey",
    {
        **{member.name: member.value for member in KitCriteriaOutputFieldKey},
        "UPLOADED_TRACKS_NOT_ARCHIVED_INTERNAL": "uploaded_tracks_not_archived",
        "UPLOADED_TRACKS_NOT_ARCHIVED_PUBLIC": "uploaded_tracks",
        "UPLOADED_TRACKS_NOT_ARCHIVED_COUNT_INTERNAL": "uploaded_tracks_not_archived_count",
        "UPLOADED_TRACKS_NOT_ARCHIVED_COUNT_PUBLIC": "uploaded_tracks_count",
        "UPLOADED_TRACKS_ARCHIVED_COUNT_INTERNAL": "uploaded_tracks_archived_count",
        "UPLOADED_TRACKS_ARCHIVED_COUNT_PUBLIC": "uploaded_tracks_archived_count",
        "UPLOADED_TRACKS_TITLE": "title",
        "CRITERIA_PLAYLIST": "criteria_playlist",
    },
)
