from rest_framework import status

from hear.test.tests.integration.playlist.children.criteria.genre.GenrePlaylistTestCase import GenrePlaylistTestCase


class TestCase(GenrePlaylistTestCase):
    def test_then_tracks_count_and_not_uploaded_tracks_count(self):
        self.model_fixture_factory.create_genre(name="Rock")

        response = self._list_genre_playlists()

        assert response.status_code == status.HTTP_200_OK
        assert self._rock()["tracksCount"] == 0
        assert "uploadedTracksCount" not in self._rock()

    def test_unaccepted_root_genre_then_is_unaccepted_root_true(self):
        self.model_fixture_factory.create_genre(name="Rock", is_unaccepted_root=True)

        response = self._list_genre_playlists()

        assert response.status_code == status.HTTP_200_OK
        assert self._rock()["isUnacceptedRoot"] is True

    def test_regular_genre_then_is_unaccepted_root_false(self):
        self.model_fixture_factory.create_genre(name="Rock")

        response = self._list_genre_playlists()

        assert response.status_code == status.HTTP_200_OK
        assert self._rock()["isUnacceptedRoot"] is False

    def _rock(self) -> dict:
        return next(item for item in self.results if item["name"] == "Rock")
