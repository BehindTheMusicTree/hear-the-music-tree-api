from django.urls import reverse

from api.model.spotify_resource.children.track.SpotifyLibTrack import SpotifyLibTrack
from api.test.tests.integration.reference.reference_test_case import ReferenceTestCase


class ReferenceSpotifyLibTrackTestCase(ReferenceTestCase):
    def test_reference_spotify_lib_track_list_then_200(self):
        self.model_fixture_factory._create_spotify_lib_track(user=self._system_user, name="tmta spotify track")
        self.model_fixture_factory._create_spotify_lib_track(user=self.test_user1, name="user1 spotify track")
        response = self.api_client.get(path=reverse('reference-spotify-lib-track-list'))
        self._assert_all_results_belong_to_tmta(response, SpotifyLibTrack)
