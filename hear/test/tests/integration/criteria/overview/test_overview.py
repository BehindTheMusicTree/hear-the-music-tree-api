from django.db import connection
from django.test.utils import CaptureQueriesContext
from rest_framework import status
from the_music_tree_api_kit.utils.data_transformer import to_camel_case

from hear.serializer.model.criteria.output.CriteriaOutputFieldKey import CriteriaOutputFieldKey
from hear.test.tests.integration.criteria.GenreTestCase import GenreTestCase


class TestCase(GenreTestCase):
    def _count_overview_queries(self, archived_tracks_count: int) -> int:
        genre = self.model_fixture_factory.create_genre(name=f"genre {archived_tracks_count}")
        for i in range(archived_tracks_count):
            self.model_fixture_factory.create_uploaded_track_with_file(title=f"t{i}", genre=genre, archived=True)
        with CaptureQueriesContext(connection) as queries:
            response = self._get_genre_overview(uuid=genre.uuid)
        assert response.status_code == status.HTTP_200_OK
        assert response.json()[to_camel_case(CriteriaOutputFieldKey.UPLOADED_TRACKS_ARCHIVED_COUNT_PUBLIC.value)] == (
            archived_tracks_count
        )
        return len(queries)

    def test_get_overview_then_only_overview_fields(self):
        genre = self.model_fixture_factory.create_genre(name="rock", side="core", summary="Loud guitars")

        response = self._get_genre_overview(uuid=genre.uuid)

        assert response.status_code == status.HTTP_200_OK
        assert response.json() == {
            CriteriaOutputFieldKey.UUID.value: str(genre.uuid),
            CriteriaOutputFieldKey.NAME.value: "rock",
            CriteriaOutputFieldKey.SUMMARY.value: "Loud guitars",
            CriteriaOutputFieldKey.SIDE.value: "core",
            to_camel_case(CriteriaOutputFieldKey.UPLOADED_TRACKS_ARCHIVED_COUNT_PUBLIC.value): 0,
        }

    def test_get_overview_of_another_user_genre_then_404(self):
        genre = self.model_fixture_factory.create_genre(name="rock")

        self._login_as_test_user2()
        response = self._get_genre_overview(uuid=genre.uuid)
        self._login_as_test_user1()

        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_get_overview_without_auth_then_401(self):
        genre = self.model_fixture_factory.create_genre(name="rock")

        self._logout()
        response = self._get_genre_overview(uuid=genre.uuid)

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_get_overview_with_many_archived_tracks_then_same_query_count_as_one(self):
        assert self._count_overview_queries(3) == self._count_overview_queries(1)
