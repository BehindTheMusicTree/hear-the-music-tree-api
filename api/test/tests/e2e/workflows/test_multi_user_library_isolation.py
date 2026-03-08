import pytest
from rest_framework import status

from api.model.criteria.children.genre.Genre import Genre
from api.model.playlist.children.manual.ManualPlaylist import ManualPlaylist
from api.model.uploaded_track.UploadedTrack import UploadedTrack
from api.serializer.model.criteria.input.post import Fields as PostFields
from api.serializer.model.playlist.children.manual.input.Fields import (
    Fields as ManualPlaylistFields,
)
from api.test.tests.integration.criteria.GenreTestCase import GenreTestCase
from api.test.tests.integration.playlist.children.manual.ManualPlaylistTestCase import (
    ManualPlaylistTestCase,
)
from api.test.utils.uploaded_track.UploadedTrackTestFilename import UploadedTrackTestFilename


@pytest.mark.e2e
class TestCase(GenreTestCase):
    """
    E2E test for multi-user library isolation.

    This test verifies the complete workflow:
    1. User 1 authenticates
    2. User 1 uploads tracks and creates genres/playlists
    3. User 2 authenticates
    4. User 2 uploads different tracks and creates different genres/playlists
    5. User 1 retrieves their library (should only see their resources)
    6. User 2 retrieves their library (should only see their resources)
    7. Verify no cross-contamination
    """

    def test_multi_user_library_isolation_then_ok(self):
        self._login_as_test_user1()
        playlist_helper = self._domain_helper(ManualPlaylistTestCase)

        user1_genre_name = "User1 Genre"
        response = self._post_genre(**{PostFields.NAME_PUBLIC: user1_genre_name})
        assert response.status_code == status.HTTP_201_CREATED
        user1_genre = self.saved_object

        user1_track = self.model_fixture_factory.create_uploaded_track_with_file(
            title="User1 Track",
            test_uploaded_track_filename=UploadedTrackTestFilename.DEFAULT_MP3,
        )

        user1_playlist_name = "User1 Playlist"
        response = playlist_helper._post_manual_playlist(
            **{ManualPlaylistFields.NAME_PUBLIC: user1_playlist_name}
        )
        assert response.status_code == status.HTTP_201_CREATED
        user1_playlist = playlist_helper.saved_object

        user1_genres = Genre.objects.filter(user=self.test_user1)
        user1_tracks = UploadedTrack.objects.filter(user=self.test_user1)
        user1_playlists = ManualPlaylist.objects.filter(user=self.test_user1)

        assert user1_genres.count() == 1
        assert user1_genres.first() == user1_genre
        assert user1_tracks.count() >= 1
        assert user1_track in user1_tracks
        assert user1_playlists.count() >= 1
        assert user1_playlist in user1_playlists

        self._login_as_test_user2()

        user2_genre_name = "User2 Genre"
        response = self._post_genre(**{PostFields.NAME_PUBLIC: user2_genre_name})
        assert response.status_code == status.HTTP_201_CREATED
        user2_genre = self.saved_object

        user2_track = self.model_fixture_factory.create_uploaded_track_with_file(
            title="User2 Track",
            test_uploaded_track_filename=UploadedTrackTestFilename.DEFAULT_MP3,
            user=self.test_user2,
        )

        user2_playlist_name = "User2 Playlist"
        response = playlist_helper._post_manual_playlist(
            **{ManualPlaylistFields.NAME_PUBLIC: user2_playlist_name}
        )
        assert response.status_code == status.HTTP_201_CREATED
        user2_playlist = playlist_helper.saved_object

        user2_genres = Genre.objects.filter(user=self.test_user2)
        user2_tracks = UploadedTrack.objects.filter(user=self.test_user2)
        user2_playlists = ManualPlaylist.objects.filter(user=self.test_user2)

        assert user2_genres.count() == 1
        assert user2_genres.first() == user2_genre
        assert user2_tracks.count() >= 1
        assert user2_track in user2_tracks
        assert user2_playlists.count() >= 1
        assert user2_playlist in user2_playlists

        assert user1_genre not in user2_genres
        assert user1_track not in user2_tracks
        assert user1_playlist not in user2_playlists

        assert user2_genre not in user1_genres
        assert user2_track not in user1_tracks
        assert user2_playlist not in user1_playlists

        self._login_as_test_user1()

        user1_genres_after = Genre.objects.filter(user=self.test_user1)
        user1_tracks_after = UploadedTrack.objects.filter(user=self.test_user1)
        user1_playlists_after = ManualPlaylist.objects.filter(user=self.test_user1)

        assert user1_genres_after.count() == 1
        assert user1_genre in user1_genres_after
        assert user1_track in user1_tracks_after
        assert user1_playlist in user1_playlists_after
        assert user2_genre not in user1_genres_after
        assert user2_track not in user1_tracks_after
        assert user2_playlist not in user1_playlists_after
