from the_music_tree_api_kit.base.BaseManager import BaseManager


class AllUploadedTrackMixinManager(BaseManager):
    def get_default_ordering(self) -> list[str]:
        return []
