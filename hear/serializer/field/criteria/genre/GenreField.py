from the_music_tree_genre_kit.serializer.field.criteria.CriteriaField import CriteriaField

from hear.model.criteria.children.genre.Genre import Genre


class GenreField(CriteriaField):
    """
    Genre-specific field that inherits from the unified CriteriaField.
    Automatically handles both UUID and name-based inputs for genres.
    """

    def __init__(self, input_types: list[str] | None = None, **kwargs):
        super().__init__(queryset=Genre.objects.all(), input_types=input_types, **kwargs)

    def to_representation(self, value):
        return super().to_representation(value)
