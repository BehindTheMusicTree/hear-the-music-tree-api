from django.urls import reverse
from rest_framework import status

from hear.test.tests.integration.spotify_lib_track.SpotifyLibTrackTestCase import SpotifyLibTrackTestCase


class TestPost(SpotifyLibTrackTestCase):
    def test_post_spotify_lib_tracks_then_405_method_not_allowed(self):
        response = self.api_client.post(path=reverse("me-spotify-lib-track-list"), data={"name": "Test Track"})
        assert response.status_code == status.HTTP_405_METHOD_NOT_ALLOWED
