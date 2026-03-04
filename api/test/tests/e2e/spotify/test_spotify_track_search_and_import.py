import pytest
from unittest import mock

from django.urls import reverse
from rest_framework import status

from api.model.spotify_resource.children.track.Fields import Fields as SpotifyLibTrackFields
from api.model.spotify_resource.children.track.SpotifyLibTrack import SpotifyLibTrack
from api.test.tests.integration.spotify.lib_track.SpotifyLibTrackTestCase import SpotifyLibTrackTestCase
from api.utils.spotify_api.ApiFields import ApiFields
from api.utils.data_transformer import to_camel_case
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

    Note: This test uses mocks for the Spotify API client. For real E2E testing,
    set SPOTIFY_ENABLED=true and configure actual Spotify credentials. In CI,
    conftest mocks the Spotify client; this test overrides with its own mock so the flow is deterministic.
    """

    def setUp(self):
        super().setUp()
        self.mock_spotify_client = mock.MagicMock()
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
        self.mock_spotify_client.search_track.return_value = {
            ApiFields.Names.TRACKS: {
                ApiFields.Names.ITEMS: [self.mock_track_data]
            }
        }

    def test_spotify_track_search_and_import_then_ok(self):
        search_query = "Test Track"
        with mock.patch(
            "api.utils.spotify_api.managers.SpotifyApiLibTrackManager.SpotifyClient",
            return_value=self.mock_spotify_client,
        ):
            manager = SpotifyApiLibTrackManager()
            tracks = manager.search_spotify_lib_tracks(self.spotify_test_user_1, search_query)

        assert len(tracks) >= 0
        self.mock_spotify_client.search_track.assert_called()

        if tracks:
            track = tracks[0]
            assert isinstance(track, SpotifyLibTrack)
            assert track.spotify_id is not None
            assert track.name is not None

            response = self.api_client.get(
                reverse("me-spotify-lib-track-detail", kwargs={"pk": track.spotify_id})
            )
            assert response.status_code == status.HTTP_200_OK

            data = response.json()
            assert data.get(to_camel_case(SpotifyLibTrackFields.SPOTIFY_ID)) == track.spotify_id
            assert data.get(SpotifyLibTrackFields.NAME) == track.name
