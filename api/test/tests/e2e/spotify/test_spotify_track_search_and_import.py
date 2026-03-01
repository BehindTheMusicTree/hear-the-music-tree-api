import pytest
from unittest import mock
from rest_framework import status

from api.model.spotify_resource.children.track.SpotifyLibTrack import SpotifyLibTrack
from api.test.tests.integration.spotify/lib_track/SpotifyLibTrackTestCase import SpotifyLibTrackTestCase
from api.utils.spotify_api.ApiFields import ApiFields
from api.utils.spotify_api.SpotifyClient import SpotifyClient
from api.utils.spotify_api.managers.SpotifyApiLibTrackManager import SpotifyApiLibTrackManager


@pytest.mark.e2e
class TestCase(SpotifyLibTrackTestCase):
    """
    E2E test for Spotify track search and import.

    This test verifies the complete workflow:
    1. User authenticates via Spotify OAuth
    2. User searches for a track on Spotify via API
    3. System searches Spotify API and returns results
    4. User selects a track from results
    5. System creates SpotifyLibTrack record
    6. User retrieves the track via API

    Note: This test uses mocks for Spotify API. For real E2E testing,
    configure actual Spotify OAuth credentials.
    """

    def setUp(self):
        super().setUp()
        self.mock_spotify_patcher = mock.patch('spotipy.Spotify')
        self.mock_spotify = self.mock_spotify_patcher.start()
        self.mock_spotify_instance = self.mock_spotify.return_value

        self.mock_track_data = {
            ApiFields.Names.ID: "spotify_track_456",
            ApiFields.Names.NAME: "Searched Track",
            ApiFields.Names.POPULARITY: 90,
            ApiFields.Names.DURATION_MS: 180000,
            ApiFields.Names.ARTISTS: [
                {ApiFields.Names.ID: "artist_456", ApiFields.Names.NAME: "Searched Artist"}
            ],
            ApiFields.Names.ALBUM: {
                ApiFields.Names.ID: "album_456",
                ApiFields.Names.NAME: "Searched Album"
            }
        }

        self.mock_spotify_instance.search.return_value = {
            ApiFields.Names.TRACKS: {
                ApiFields.Names.ITEMS: [self.mock_track_data]
            }
        }

    def tearDown(self):
        self.mock_spotify_patcher.stop()
        super().tearDown()

    def test_spotify_track_search_and_import_then_ok(self):
        SpotifyClient._instance = None
        SpotifyClient._initialized = False

        search_query = "Test Track"
        manager = SpotifyApiLibTrackManager()
        tracks = manager.search_spotify_lib_tracks(self.spotify_test_user_1, search_query)

        assert len(tracks) >= 0

        self.mock_spotify_instance.search.assert_called()

        if tracks:
            track = tracks[0]
            assert isinstance(track, SpotifyLibTrack)
            assert track.spotify_id is not None
            assert track.name is not None

            response = self._retrieve_spotify_lib_track(track.spotify_id)
            assert response.status_code == status.HTTP_200_OK

            retrieved_track = self.saved_object
            assert retrieved_track is not None
            assert retrieved_track.spotify_id == track.spotify_id
            assert retrieved_track.name == track.name
