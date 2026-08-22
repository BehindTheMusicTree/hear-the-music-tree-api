from rest_framework import status

from hear.model.criteria.Criteria import Fields
from hear.test.tests.integration.criteria.GenreTestCase import GenreTestCase


class TestCase(GenreTestCase):
    def test_name(self):
        genre_name = "Rock"
        self.model_fixture_factory.create_genre(name=genre_name)

        response = self._list_genres()

        assert response.status_code == status.HTTP_200_OK
        assert self.results_overall_total == 1
        genre_rock_json = self.results[0]
        assert genre_rock_json[Fields.NAME_PUBLIC] == genre_name
