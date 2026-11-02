from datetime import timedelta
from unittest import mock

from django.utils import timezone

from hear.model.spotify_resource.children.track.SpotifyLibTrack import SpotifyLibTrack
from hear.test.tests.integration.spotify.lib_track.SpotifyLibTrackTestCase import SpotifyLibTrackTestCase
from hear.utils.spotify_api.ApiFields import ApiFields
from hear.utils.spotify_api.managers.SpotifyApiLibTrackManager import SpotifyApiLibTrackManager


class TestCase(SpotifyLibTrackTestCase):
    def _full_sync(self, track_data: dict) -> None:
        self.spotify_test_user_1.spotify_access_token = "access-token"
        client = mock.MagicMock()
        client.get_user_saved_tracks.side_effect = [
            {ApiFields.Names.ITEMS: [{ApiFields.Names.TRACK: track_data}]},
            {ApiFields.Names.ITEMS: []},
        ]
        with mock.patch(
            "hear.utils.spotify_api.managers.SpotifyApiLibTrackManager.get_spotify_client", return_value=client
        ):
            SpotifyApiLibTrackManager().full_sync(self.spotify_test_user_1)

    def test_full_sync_of_unchanged_existing_track_persists_last_synced_at_and_is_removed(self):
        track_data = {
            ApiFields.Names.ID: "spotify_track_sync",
            ApiFields.Names.NAME: "Sync Track",
            ApiFields.Names.POPULARITY: 50,
            ApiFields.Names.DURATION_MS: 200000,
            ApiFields.Names.ARTISTS: [{ApiFields.Names.ID: "artist_sync", ApiFields.Names.NAME: "Sync Artist"}],
            ApiFields.Names.ALBUM: {ApiFields.Names.ID: "album_sync", ApiFields.Names.NAME: "Sync Album"},
        }
        self._full_sync(track_data)
        stale = timezone.now() - timedelta(days=30)
        SpotifyLibTrack.objects.filter(spotify_id="spotify_track_sync").update(is_removed=True, last_synced_at=stale)

        self._full_sync(track_data)

        track = SpotifyLibTrack.objects.get(spotify_id="spotify_track_sync")
        assert track.is_removed is False
        assert track.last_synced_at > stale
