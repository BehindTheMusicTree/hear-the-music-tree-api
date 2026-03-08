from rest_framework import status
from django.urls import reverse

from api.test.tests.integration.spotify_lib_track.SpotifyLibTrackTestCase import SpotifyLibTrackTestCase


class TestDelete(SpotifyLibTrackTestCase):
    def test_delete_spotify_lib_tracks_then_405_method_not_allowed(self):
        response = self.api_client.delete(
            path=reverse('me-spotify-lib-track-list')
        )
        assert response.status_code == status.HTTP_405_METHOD_NOT_ALLOWED
