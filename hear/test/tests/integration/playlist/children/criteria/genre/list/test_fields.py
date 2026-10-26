from rest_framework import status

from hear.serializer.model.playlist.children.criteria.output.detailed import Fields as RietrieveFields
from hear.test.tests.integration.playlist.children.criteria.genre.GenrePlaylistTestCase import GenrePlaylistTestCase


class TestCase(GenrePlaylistTestCase):
    def test_then_tracks_count_and_not_uploaded_tracks_count(self):
        self.model_fixture_factory.create_genre(name="Rock")

        response = self._list_genre_playlists()

        assert response.status_code == status.HTTP_200_OK
        assert self.results[0][RietrieveFields.TRACKS_COUNT_PUBLIC] == 0
        assert "uploaded_tracks_count" not in self.results[0]

    def test_unaccepted_root_genre_then_is_unaccepted_root_true(self):
        genre = self.model_fixture_factory.create_genre(name="Rock")
        genre.is_unaccepted_root = True
        genre.save()

        response = self._list_genre_playlists()

        assert response.status_code == status.HTTP_200_OK
        assert self.results[0][RietrieveFields.IS_UNACCEPTED_ROOT] is True

    def test_regular_genre_then_is_unaccepted_root_false(self):
        self.model_fixture_factory.create_genre(name="Rock")

        response = self._list_genre_playlists()

        assert response.status_code == status.HTTP_200_OK
        assert self.results[0][RietrieveFields.IS_UNACCEPTED_ROOT] is False
