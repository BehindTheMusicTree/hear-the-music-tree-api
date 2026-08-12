from typing import TYPE_CHECKING, Any, Self

from the_music_tree_genre_kit.criteria.type.CriteriaType import CriteriaType
from the_music_tree_genre_kit.criteria.type.CriteriaTypePks import CriteriaTypePks

from ...CriteriaManager import CriteriaManager

if TYPE_CHECKING:
    from .Tag import Tag


class TagManager(CriteriaManager):
    model: Tag

    def _get_criteria_type(self) -> CriteriaType:
        return CriteriaType(pk=CriteriaTypePks.TAG)

    def create(self, **kwargs) -> Tag:
        return super().create(type_id=CriteriaTypePks.TAG, **kwargs)

    def filter(self, *args: Any, **kwargs: Any) -> Self:
        return super().filter(type_id=CriteriaTypePks.TAG, *args, **kwargs)
