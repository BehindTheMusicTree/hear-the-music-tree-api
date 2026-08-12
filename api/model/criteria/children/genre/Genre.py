from the_music_tree_genre_kit.criteria.type.CriteriaType import CriteriaType
from the_music_tree_genre_kit.criteria.type.CriteriaTypePks import CriteriaTypePks

from api.model.criteria.Criteria import Criteria

from .GenreManager import GenreManager


class Genre(Criteria):
    objects: GenreManager = GenreManager()

    class Meta:
        db_table = "htmt_api_genre"
        proxy = True

    def save(self, *args, **kwargs):
        self.type = CriteriaType.objects.get(pk=CriteriaTypePks.GENRE)
        super().save(*args, **kwargs)
