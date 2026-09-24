from typing import TYPE_CHECKING

from the_music_tree_genre_kit.criteria.children.tag.AbstractTagManager import AbstractTagManager

from ...CriteriaManager import CriteriaManager

if TYPE_CHECKING:
    from .Tag import Tag


class TagManager(AbstractTagManager, CriteriaManager):
    model: Tag
