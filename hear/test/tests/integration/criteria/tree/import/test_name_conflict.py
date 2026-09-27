from typing import cast

from rest_framework import status

from hear.model.criteria.children.genre.Genre import Genre
from hear.serializer.model.criteria.input.tree_import import Fields
from hear.test.tests.integration.criteria.GenreTestCase import GenreTestCase


class TestNameConflict(GenreTestCase):
    def test_duplicate_name_is_flagged_instead_of_failing_import(self):
        initial_genre = self.model_fixture_factory.create_genre(name="Initial Rock")
        initial_genre_id = initial_genre.uuid

        tree_data = [
            {
                Fields.NAME_PUBLIC: "Rock",
                Fields.CHILDREN: [
                    {Fields.NAME_PUBLIC: "Punk", Fields.CHILDREN: []},
                    {Fields.NAME_PUBLIC: "Rock", Fields.CHILDREN: []},
                ],
            }
        ]
        response = self._post_genres_tree_import(data={Fields.TREE: tree_data})

        assert response.status_code == status.HTTP_201_CREATED
        genres = Genre.objects.filter(user=self.test_user1)
        assert genres.count() == 4
        assert genres.filter(has_name_conflict=True).count() == 1
        genre = cast(Genre, genres.get(uuid=initial_genre_id))
        assert genre.name == "Initial Rock"
