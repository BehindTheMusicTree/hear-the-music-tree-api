from rest_framework import status

from hear.serializer.model.playlist.children.criteria.output.detailed import Fields as RietrieveFields
from hear.test.tests.integration.playlist.children.criteria.genre.GenrePlaylistTestCase import GenrePlaylistTestCase


class TestCase(GenrePlaylistTestCase):
    def test_false_then_only_canonical_tree(self):
        genre_rock = self.model_fixture_factory.create_genre(name="Rock")
        self.model_fixture_factory.create_genre(name="Italian progressive rock", allows_multiple_primary_parents=True)

        response = self._list_genre_playlists(allows_multiple_primary_parents="false")

        assert response.status_code == status.HTTP_200_OK
        assert [result[RietrieveFields.NAME] for result in self.results] == [genre_rock.name]
