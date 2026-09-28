from rest_framework import status
from the_music_tree_api_kit.utils.data_transformer import to_camel_case

from hear.serializer.model.criteria.output.CriteriaOutputFieldKey import CriteriaOutputFieldKey
from hear.test.tests.integration.criteria.GenreTestCase import GenreTestCase


class TestCase(GenreTestCase):
    def test_name(self):
        name = "rock"
        uuid = self.model_fixture_factory.create_genre(name=name).uuid

        response = self._retrieve_genre(uuid=uuid)

        assert response.status_code == status.HTTP_200_OK
        assert self.result[CriteriaOutputFieldKey.NAME.value] == name

    def test_side(self):
        side = "core"
        uuid = self.model_fixture_factory.create_genre(name="rock", side=side).uuid

        response = self._retrieve_genre(uuid=uuid)

        assert response.status_code == status.HTTP_200_OK
        assert self.result[CriteriaOutputFieldKey.SIDE.value] == side

    def test_uploaded_tracks_count_without_track_list(self):
        criteria = self.model_fixture_factory.create_genre(name="rock")
        for title in ("stylax", "bien"):
            self.model_fixture_factory.create_uploaded_track_with_file(
                title=title, genre=criteria, use_manager_for_genre_playlist_adding=True
            )

        response = self._retrieve_genre(uuid=criteria.uuid)

        assert response.status_code == status.HTTP_200_OK
        assert self.result[to_camel_case(CriteriaOutputFieldKey.UPLOADED_TRACKS_NOT_ARCHIVED_COUNT_PUBLIC.value)] == 2
        assert to_camel_case(CriteriaOutputFieldKey.UPLOADED_TRACKS_NOT_ARCHIVED_PUBLIC.value) not in self.result
