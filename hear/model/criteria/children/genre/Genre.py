from django.db import models
from the_music_tree_api_kit.field.foreign_key.PrivateOneToOneField import PrivateOneToOneField
from the_music_tree_genre_kit.criteria.children.genre.AbstractGenreCriteria import AbstractGenreCriteria
from the_music_tree_genre_kit.criteria.type.CriteriaType import CriteriaType
from the_music_tree_genre_kit.criteria.type.CriteriaTypePks import CriteriaTypePks

from hear.model.criteria.Criteria import Criteria

from .GenreManager import GenreManager


class Genre(AbstractGenreCriteria, Criteria):  # type: ignore[django-manager-missing]
    criteria_ptr = PrivateOneToOneField(Criteria, on_delete=models.CASCADE, parent_link=True, related_name="genre")

    objects: GenreManager = GenreManager()

    class Meta:
        db_table = "htmt_api_genre"

    def save(self, *args, **kwargs):
        self.type = CriteriaType.objects.get(pk=CriteriaTypePks.GENRE)
        super().save(*args, **kwargs)
