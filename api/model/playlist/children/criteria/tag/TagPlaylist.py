from api.model.playlist.children.criteria.CriteriaPlaylist import CriteriaPlaylist

from .TagPlaylistManager import TagPlaylistManager


class TagPlaylist(CriteriaPlaylist):
    objects: TagPlaylistManager = TagPlaylistManager()

    class Meta:
        db_table = "htmt_api_tag_playlist"
        proxy = True
