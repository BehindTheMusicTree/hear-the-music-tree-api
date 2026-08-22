from typing import TYPE_CHECKING

from the_music_tree_genre_kit.criteria.type.CriteriaType import CriteriaType
from the_music_tree_genre_kit.criteria.type.CriteriaTypePks import CriteriaTypePks

from ...CriteriaManager import CriteriaManager

if TYPE_CHECKING:
    from .Genre import Genre


class GenreManager(CriteriaManager):
    model: Genre

    def _get_criteria_type(self) -> CriteriaType:
        return CriteriaType(pk=CriteriaTypePks.GENRE)

    def _get_direct_tracks(self, instance: Genre) -> list:
        return list(instance.uploaded_tracks.all())
