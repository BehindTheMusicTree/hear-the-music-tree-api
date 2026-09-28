from rest_framework import status
from the_music_tree_api_kit.utils import data_transformer

from hear.model.playlist.children.criteria.CriteriaPlaylist import CriteriaPlaylist
from hear.serializer.model.playlist.base.output.detailed import Fields as PlaylistOutputFields
from hear.test.tests.integration.playlist.base.PlaylistTestCase import PlaylistTestCase
from hear.test.utils.uploaded_track.UploadedTrackTestFilename import UploadedTrackTestFilename


class TestCase(PlaylistTestCase):
    def test_retrieve_then_no_track_playlist_relations(self):
        genre = self.model_fixture_factory.create_genre(name="rock")
        self.model_fixture_factory.create_uploaded_track_with_file(
            title="Love", genre=genre, use_manager_for_genre_playlist_adding=True
        )

        response = self._retrieve_playlist(uuid=genre.criteria_playlist.uuid)

        assert response.status_code == status.HTTP_200_OK
        assert "uploadedTrackPlaylistRelations" not in response.json()

    def test_duration(self):
        genre = self.model_fixture_factory.create_genre(name="rock")
        genre_criteria_playlist: CriteriaPlaylist = genre.criteria_playlist
        self.model_fixture_factory.create_uploaded_track_with_file(
            title="celine",
            genre=genre,
            test_uploaded_track_filename=UploadedTrackTestFilename.DURATION_472S_WAV,
            use_manager_for_genre_playlist_adding=True,
        )
        self.model_fixture_factory.create_uploaded_track_with_file(
            title="celine",
            genre=genre,
            test_uploaded_track_filename=UploadedTrackTestFilename.DURATION_277S_MP3,
            use_manager_for_genre_playlist_adding=True,
        )

        response = self._retrieve_playlist(genre_criteria_playlist.uuid)

        assert response.status_code == status.HTTP_200_OK
        assert self.result[data_transformer.to_camel_case(PlaylistOutputFields.DURATION_IN_SEC)] == 472 + 277

    def test_count(self):
        genre = self.model_fixture_factory.create_genre(name="rock")
        self.model_fixture_factory.create_uploaded_track_with_file(
            title="In Too Deep", genre=genre, use_manager_for_genre_playlist_adding=True
        )
        self.model_fixture_factory.create_uploaded_track_with_file(
            title="Summer", genre=genre, use_manager_for_genre_playlist_adding=True
        )
        self.model_fixture_factory.create_uploaded_track_with_file(
            title="Winter", genre=genre, archived=True, use_manager_for_genre_playlist_adding=True
        )

        response = self._retrieve_playlist(genre.criteria_playlist.uuid)

        assert response.status_code == status.HTTP_200_OK
        assert (
            self.result[data_transformer.to_camel_case(PlaylistOutputFields.UPLOADED_TRACKS_NOT_ARCHIVED_COUNT_PUBLIC)]
            == 2
        )

    def test_archived_count(self):
        genre = self.model_fixture_factory.create_genre(name="rock")
        self.model_fixture_factory.create_uploaded_track_with_file(
            title="In Too Deep", genre=genre, use_manager_for_genre_playlist_adding=True
        )
        self.model_fixture_factory.create_uploaded_track_with_file(
            title="Summer", genre=genre, archived=True, use_manager_for_genre_playlist_adding=True
        )
        self.model_fixture_factory.create_uploaded_track_with_file(
            title="Summer2", genre=genre, use_manager_for_genre_playlist_adding=True
        )
        self.model_fixture_factory.create_uploaded_track_with_file(
            title="Summer3", genre=genre, archived=True, use_manager_for_genre_playlist_adding=True
        )

        response = self._retrieve_playlist(genre.criteria_playlist.uuid)

        assert response.status_code == status.HTTP_200_OK
        assert (
            self.result[data_transformer.to_camel_case(PlaylistOutputFields.UPLOADED_TRACKS_ARCHIVED_COUNT_PUBLIC)] == 2
        )
