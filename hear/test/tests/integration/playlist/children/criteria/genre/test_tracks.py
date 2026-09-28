from django.urls import reverse
from rest_framework import status
from the_music_tree_api_kit.view.pagination.PaginatedResponseFields import PaginatedResponseFields

from hear.test.tests.integration.playlist.children.criteria.genre.GenrePlaylistTestCase import GenrePlaylistTestCase


class TestCase(GenrePlaylistTestCase):
    def test_tracks_page_then_position_ordered_and_paginated(self):
        genre = self.model_fixture_factory.create_genre(name="rock")
        for title in ("a", "b", "c"):
            self.model_fixture_factory.create_uploaded_track_with_file(
                title=title, genre=genre, use_manager_for_genre_playlist_adding=True
            )
        path = reverse("me-genre-playlist-tracks", kwargs={"pk": genre.criteria_playlist.uuid})

        first = self.api_client.get(path=path, data={"pageSize": 2}).json()
        second = self.api_client.get(path=path, data={"pageSize": 2, "page": 2}).json()

        assert first[PaginatedResponseFields.OVERALL_TOTAL] == 3
        assert first[PaginatedResponseFields.NEXT] is not None
        rels = first[PaginatedResponseFields.RESULTS] + second[PaginatedResponseFields.RESULTS]
        assert [rel["position"] for rel in rels] == [1, 2, 3]
        assert {rel["track"]["title"] for rel in rels} == {"a", "b", "c"}
        assert "playlists" not in rels[0]["track"]

    def test_tracks_page_of_another_user_playlist_then_404(self):
        genre = self.model_fixture_factory.create_genre(name="rock")

        self._login_as_test_user2()
        response = self.api_client.get(
            path=reverse("me-genre-playlist-tracks", kwargs={"pk": genre.criteria_playlist.uuid})
        )

        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_tracks_page_with_archived_track_then_hidden(self):
        genre = self.model_fixture_factory.create_genre(name="rock")
        for title in ("kept", "archived"):
            track = self.model_fixture_factory.create_uploaded_track_with_file(
                title=title, genre=genre, use_manager_for_genre_playlist_adding=True
            )
        track.archived = True
        track.save(update_fields=["archived"])

        page = self.api_client.get(
            path=reverse("me-genre-playlist-tracks", kwargs={"pk": genre.criteria_playlist.uuid})
        ).json()

        assert page[PaginatedResponseFields.OVERALL_TOTAL] == 1
        assert page[PaginatedResponseFields.RESULTS][0]["track"]["title"] == "kept"
