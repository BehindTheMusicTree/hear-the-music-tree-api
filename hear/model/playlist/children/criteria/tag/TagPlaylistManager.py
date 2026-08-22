from the_music_tree_genre_kit.criteria.type.CriteriaTypePks import CriteriaTypePks

from hear.model.playlist.children.criteria.CriteriaPlaylistManager import CriteriaPlaylistManager


class TagPlaylistManager(CriteriaPlaylistManager):
    def get_queryset(self):
        return super().get_queryset().filter(type_id=CriteriaTypePks.TAG)
