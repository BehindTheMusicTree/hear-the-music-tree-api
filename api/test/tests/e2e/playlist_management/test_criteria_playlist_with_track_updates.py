import pytest
from rest_framework import status

from api.model.criteria.children.genre.Genre import Genre
from api.model.playlist.children.criteria.CriteriaPlaylist import CriteriaPlaylist
from api.serializer.model.criteria.input.post import Fields as PostFields
from api.serializer.model.uploaded_track.input.put.Fields import Fields as PutFields
from api.test.utils.AppTestCase import AppTestCase
from api.test.utils.uploaded_track.UploadedTrackTestFilename import UploadedTrackTestFilename


@pytest.mark.e2e
class TestCase(AppTestCase):
    """
    E2E test for criteria playlist with track updates.

    This test verifies the complete workflow:
    1. User authenticates
    2. User creates a genre "Rock"
    3. System automatically creates genre playlist
    4. User uploads a track and tags it with "Rock"
    5. Track appears in "Rock" playlist
    6. User changes track genre to "Jazz"
    7. Track is removed from "Rock" playlist
    8. User creates "Jazz" genre
    9. Track appears in "Jazz" playlist
    """

    def test_criteria_playlist_with_track_updates_then_ok(self):
        from api.test.tests.integration.criteria.GenreTestCase import GenreTestCase
        from api.test.tests.integration.uploaded_track.UploadedTrackTestCase import UploadedTrackTestCase

        genre_test_case = GenreTestCase()
        genre_test_case.setUp()
        genre_test_case.api_client = self.api_client
        genre_test_case._login_as_test_user1()

        uploaded_track_test_case = UploadedTrackTestCase()
        uploaded_track_test_case.setUp()
        uploaded_track_test_case.api_client = self.api_client
        uploaded_track_test_case._login_as_test_user1()

        rock_genre_name = "Rock"
        jazz_genre_name = "Jazz"

        response = genre_test_case._post_genre(**{PostFields.NAME_PUBLIC: rock_genre_name})
        assert response.status_code == status.HTTP_201_CREATED
        rock_genre = genre_test_case.saved_object

        rock_playlist = CriteriaPlaylist.objects.get(user=self.test_user1, criteria=rock_genre)
        assert rock_playlist is not None

        track = self.model_fixture_factory.create_uploaded_track_with_file(
            title="Test Track", test_uploaded_track_filename=UploadedTrackTestFilename.DEFAULT_MP3)

        response = uploaded_track_test_case._put_uploaded_track(track.uuid, **{PutFields.GENRE: rock_genre_name})
        assert response.status_code == status.HTTP_200_OK

        track.refresh_from_db()
        assert track.genre == rock_genre

        track_playlists = [p.uuid for p in track.playlists.all()]
        assert rock_playlist.playlist.uuid in track_playlists
        assert track in rock_playlist.playlist.uploaded_tracks.all()

        response = genre_test_case._post_genre(**{PostFields.NAME_PUBLIC: jazz_genre_name})
        assert response.status_code == status.HTTP_201_CREATED
        jazz_genre = genre_test_case.saved_object

        response = uploaded_track_test_case._put_uploaded_track(track.uuid, **{PutFields.GENRE: jazz_genre_name})
        assert response.status_code == status.HTTP_200_OK

        track.refresh_from_db()
        assert track.genre == jazz_genre

        track_playlists = [p.uuid for p in track.playlists.all()]
        assert rock_playlist.playlist.uuid not in track_playlists

        jazz_playlist = CriteriaPlaylist.objects.get(user=self.test_user1, criteria=jazz_genre)
        assert jazz_playlist.playlist.uuid in track_playlists
        assert track in jazz_playlist.playlist.uploaded_tracks.all()
        assert track not in rock_playlist.playlist.uploaded_tracks.all()
