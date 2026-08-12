from the_music_tree_genre_kit.serializer.field.criteria.CriteriaField import CriteriaField
from the_music_tree_genre_kit.serializer.field.criteria.CriteriaFieldInputType import CriteriaFieldInputType

from api.model.criteria.children.genre.Genre import Genre


class GenreField(CriteriaField):
    def __init__(self, input_types: list[CriteriaFieldInputType], **kwargs):
        super().__init__(queryset=Genre.objects.all(), input_types=input_types, **kwargs)
