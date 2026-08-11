from uuid import UUID

from rest_framework import status
from the_music_tree_api_kit.utils.data_transformer import to_camel_case

from api.serializer.model.criteria.output.CriteriaOutputFieldKey import CriteriaOutputFieldKey
from api.test.tests.integration.criteria.GenreTestCase import GenreTestCase


class TestCase(GenreTestCase):
    def test_name(self):
        name = "rock"
        uuid = self.model_fixture_factory.create_genre(name=name).uuid

        response = self._retrieve_genre(uuid=uuid)

        assert response.status_code == status.HTTP_200_OK
        assert self.result[CriteriaOutputFieldKey.NAME.value] == name

    def test_uploaded_tracks(self):
        criteria = self.model_fixture_factory.create_genre(name="rock")

        title1 = "stylax"
        track1_uuid = self.model_fixture_factory.create_uploaded_track_with_file(
            title=title1, genre=criteria, use_manager_for_genre_playlist_adding=True
        ).uuid

        title2 = "bien"
        track2_uuid = self.model_fixture_factory.create_uploaded_track_with_file(
            title=title2, genre=criteria, use_manager_for_genre_playlist_adding=True
        ).uuid

        response = self._retrieve_genre(uuid=criteria.uuid)

        assert response.status_code == status.HTTP_200_OK
        uploaded_tracks = self.result[to_camel_case(CriteriaOutputFieldKey.UPLOADED_TRACKS_NOT_ARCHIVED_PUBLIC.value)]
        assert len(uploaded_tracks) == 2
        titles = [track[CriteriaOutputFieldKey.UPLOADED_TRACKS_TITLE.value] for track in uploaded_tracks]
        assert title1 in titles
        assert title2 in titles
        uuids = [UUID(track[CriteriaOutputFieldKey.UUID.value]) for track in uploaded_tracks]
        assert track1_uuid in uuids
        assert track2_uuid in uuids
