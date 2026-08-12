from api.model.criteria.Criteria import Criteria
from the_music_tree_genre_kit.criteria.type.CriteriaType import CriteriaType
from the_music_tree_genre_kit.criteria.type.CriteriaTypePks import CriteriaTypePks

from .TagManager import TagManager


class Tag(Criteria):
    objects: TagManager = TagManager()

    class Meta:
        db_table = "htmt_api_tag"
        proxy = True

    def save(self, *args, **kwargs):
        self.type = CriteriaType.objects.get(pk=CriteriaTypePks.TAG)
        super().save(*args, **kwargs)
