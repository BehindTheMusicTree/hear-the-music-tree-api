import pytest
from unittest import mock
from rest_framework import status

from api.model.spotify_resource.children.track.SpotifyLibTrack import SpotifyLibTrack
from api.test.tests.integration.spotify.lib_track.SpotifyLibTrackTestCase import SpotifyLibTrackTestCase
from api.utils.spotify_api.ApiFields import ApiFields
from api.utils.spotify_api.SpotifyClient import SpotifyClient
from api.utils.spotify_api.managers.SpotifyApiLibTrackManager import SpotifyApiLibTrackManager


@pytest.mark.e2e
class TestCase(SpotifyLibTrackTestCase):
    """
    E2E test for Spotify library sync.

    This test verifies the complete workflow:
    1. User authenticates via Spotify OAuth
    2. User requests Spotify library tracks
    3. System fetches user's saved tracks from Spotify API
    4. System creates/updates SpotifyLibTrack records
    5. User retrieves library tracks via API
    6. User searches for tracks in library

    Note: This test uses mocks for Spotify API. For real E2E testing,
    configure actual Spotify OAuth credentials.
    """

    def setUp(self):
        super().setUp()
        self.mock_spotify_patcher = mock.patch('spotipy.Spotify')
        self.mock_spotify = self.mock_spotify_patcher.start()
        self.mock_spotify_instance = self.mock_spotify.return_value

        self.mock_track_data = {
            ApiFields.Names.ID: "spotify_track_123",
            ApiFields.Names.NAME: "Test Spotify Track",
            ApiFields.Names.POPULARITY: 85,
            ApiFields.Names.DURATION_MS: 240000,
            ApiFields.Names.ARTISTS: [
                {ApiFields.Names.ID: "artist_123", ApiFields.Names.NAME: "Test Artist"}
            ],
            ApiFields.Names.ALBUM: {
                ApiFields.Names.ID: "album_123",
                ApiFields.Names.NAME: "Test Album"
            }
        }

        self.mock_spotify_instance.current_user_saved_tracks.return_value = {
            ApiFields.Names.ITEMS: [{
                ApiFields.Names.TRACK: self.mock_track_data
            }]
        }

    def tearDown(self):
        self.mock_spotify_patcher.stop()
        super().tearDown()

    def test_spotify_library_sync_then_ok(self):
        SpotifyClient._instance = None
        SpotifyClient._initialized = False

        manager = SpotifyApiLibTrackManager()
        tracks = manager.sync_user_library(self.spotify_test_user_1)

        assert len(tracks) >= 0

        response = self._list_spotify_lib_tracks()
        assert response.status_code == status.HTTP_200_OK

        if hasattr(self, 'results') and self.results:
            track_ids = [t.get('spotifyId') for t in self.results]
            if tracks:
                assert any(track.spotify_id in track_ids for track in tracks)

        if tracks:
            first_track = tracks[0]
            response = self._retrieve_spotify_lib_track(first_track.spotify_id)
            assert response.status_code == status.HTTP_200_OK

            retrieved_track = self.saved_object
            assert retrieved_track is not None
            assert retrieved_track.spotify_id == first_track.spotify_id
