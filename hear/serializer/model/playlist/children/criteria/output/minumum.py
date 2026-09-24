from the_music_tree_genre_kit.serializer.model.criteria.playlist.output.minimum import (
    build_criteria_playlist_minimum_serializer,
)

from hear.model.playlist.children.criteria.CriteriaPlaylist import CriteriaPlaylist

CriteriaPlaylistMinimumSerializer = build_criteria_playlist_minimum_serializer(CriteriaPlaylist)
