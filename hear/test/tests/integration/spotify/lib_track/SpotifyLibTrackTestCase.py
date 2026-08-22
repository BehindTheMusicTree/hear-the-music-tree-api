from django.http import HttpResponse
from django.urls import reverse

from hear.model.spotify_resource.children.track.SpotifyLibTrack import SpotifyLibTrack
from hear.test.utils.AppTestCase import AppTestCase


class SpotifyLibTrackTestCase(AppTestCase[SpotifyLibTrack]):
    model_class = SpotifyLibTrack
    saved_object: SpotifyLibTrack

    def setUp(self):
        super().setUp()
        self._login_as_spotify_test_user_1()

    def _list_spotify_lib_tracks(self, **kwargs) -> HttpResponse:
        return self.api_client.get(reverse("me-spotify-lib-track-list"), data=kwargs, handle_response=self._set_results)

    def _retrieve_spotify_lib_track(self, spotify_id: str) -> HttpResponse:
        return self.api_client.get(
            reverse("me-spotify-lib-track-detail", kwargs={"pk": spotify_id}), handle_response=self._set_results
        )
