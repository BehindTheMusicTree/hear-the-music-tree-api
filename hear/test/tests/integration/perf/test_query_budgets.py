from collections.abc import Callable

from django.db import connection
from django.test.utils import CaptureQueriesContext
from django.urls import reverse
from rest_framework import status

from hear.model.criteria.children.genre.Genre import Genre
from hear.model.playlist.children.manual.ManualPlaylist import ManualPlaylist
from hear.test.utils.AppTestCase import AppTestCase


class TestCase(AppTestCase[ManualPlaylist]):
    model_class = ManualPlaylist
    """Each endpoint's query count must not grow with the number of rows it serializes."""

    genre: Genre
    manual_playlist: ManualPlaylist
    seeded = 0

    def setUp(self):
        super().setUp()
        self.genre = self.model_fixture_factory.create_genre(name="rock")
        self.manual_playlist = self.model_fixture_factory.create_manual_playlist(name="mix")

    def _seed(self, count: int) -> None:
        for _ in range(count):
            self.seeded += 1
            track = self.model_fixture_factory.create_uploaded_track_with_file(
                title=f"t{self.seeded}", genre=self.genre, use_manager_for_genre_playlist_adding=True
            )
            track.artists.add(self.model_fixture_factory.create_artist(name=f"a{self.seeded}"))
            self.model_fixture_factory.create_uploaded_track_playlist_rel(self.manual_playlist, track)
            self.model_fixture_factory.create_play(track)
            self.model_fixture_factory.create_play(self.manual_playlist)
            self.model_fixture_factory.create_manual_playlist(name=f"p{self.seeded}")
            sub_genre = self.model_fixture_factory.create_genre(name=f"g{self.seeded}", parent=self.genre)
            self.model_fixture_factory.create_play(sub_genre.criteria_playlist)

    def _count(self, path: Callable[[], str]) -> int:
        with CaptureQueriesContext(connection) as queries:
            response = self.api_client.get(path=path())
        assert response.status_code == status.HTTP_200_OK, response.content
        return len(queries)

    def _assert_constant(self, path: Callable[[], str]) -> None:
        self._seed(2)
        self._count(path)  # warm the ContentType cache, which would otherwise count as extra queries
        small = self._count(path)
        self._seed(10)
        assert self._count(path) == small

    def test_playlist_list(self):
        self._assert_constant(lambda: reverse("me-playlist-list"))

    def test_manual_playlist_list(self):
        self._assert_constant(lambda: reverse("me-manual-playlist-list"))

    def test_genre_playlist_list(self):
        self._assert_constant(lambda: reverse("me-genre-playlist-list"))

    def test_uploaded_track_list(self):
        self._assert_constant(lambda: reverse("me-uploaded-track-list"))

    def test_play_list(self):
        self._assert_constant(lambda: reverse("me-play-list"))

    def test_genre_playlist_detail(self):
        self._assert_constant(
            lambda: reverse("me-genre-playlist-detail", kwargs={"pk": self.genre.criteria_playlist.uuid})
        )

    def test_manual_playlist_detail(self):
        self._assert_constant(lambda: reverse("me-manual-playlist-detail", kwargs={"pk": self.manual_playlist.uuid}))

    def test_genre_detail(self):
        self._assert_constant(lambda: reverse("me-genre-detail", kwargs={"pk": self.genre.uuid}))

    def test_genre_playlist_tracks(self):
        self._assert_constant(
            lambda: reverse("me-genre-playlist-tracks", kwargs={"pk": self.genre.criteria_playlist.uuid})
        )

    def test_manual_playlist_tracks(self):
        self._assert_constant(lambda: reverse("me-manual-playlist-tracks", kwargs={"pk": self.manual_playlist.uuid}))
