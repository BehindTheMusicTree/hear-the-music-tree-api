from typing import cast

from django.test import override_settings
from rest_framework import status
from the_music_tree_genre_kit.criteria.children.genre.CriteriaSource import CriteriaSource

from hear.model.criteria.children.genre.Genre import Genre
from hear.serializer.model.criteria.input.tree_import import Fields
from hear.test.tests.integration.criteria.GenreTestCase import GenreTestCase


# Full-tree replacement is what's under test, not the stale-delete guard.
@override_settings(CRITERIA_TREE_IMPORT_STALE_DELETE_MAX_FRACTION=1.0)
class TestOverwrite(GenreTestCase):
    def test_import_new_tree_then_overwrites_existing(self):
        self.model_fixture_factory.create_genre(name="Old Rock", wikidata_id="Q1", source=CriteriaSource.PIPELINE)

        tree_data = [{Fields.NAME_PUBLIC: "New Rock", Fields.CHILDREN: []}]
        response = self._post_genres_tree_import(data={Fields.TREE: tree_data})

        assert response.status_code == status.HTTP_201_CREATED

        genres = Genre.objects.filter(user=self.test_user1)
        assert genres.count() == 1
        assert cast(Genre, genres.first()).name == "New Rock"
