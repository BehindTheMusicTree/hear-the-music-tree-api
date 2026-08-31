from typing import TYPE_CHECKING

from the_music_tree_genre_kit.criteria.children.genre.AbstractGenreManager import AbstractGenreManager

from ...CriteriaManager import CriteriaManager

if TYPE_CHECKING:
    from .Genre import Genre


class GenreManager(AbstractGenreManager, CriteriaManager):
    model: Genre

    def _get_direct_tracks(self, instance: Genre) -> list:
        return list(instance.tracks.all())
