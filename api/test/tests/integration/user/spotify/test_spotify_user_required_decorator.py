from rest_framework import status

from api.test.utils.AppTestCase import AppTestCase
from api.view.error.ApiErrorCode import ApiErrorCodeNumeric


class TestSpotifyUserRequiredDecoratorIntegration(AppTestCase):
    def test_spotify_user_list_without_auth_then_401_auth_not_authenticated(self):
        self._logout()
        url = self._spotify_user_list_url()

        response = self.api_client.get(url)

        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        data = response.json()
        assert data["code"] == ApiErrorCodeNumeric.AUTH_NOT_AUTHENTICATED
        assert data["details"]["code"] == "authentication_required"
        assert data["success"] is False

    def test_spotify_user_list_with_base_user_then_403_spotify_not_authenticated(self):
        self._login_as_user(self.test_user1)
        url = self._spotify_user_list_url()

        response = self.api_client.get(url)

        assert response.status_code == status.HTTP_403_FORBIDDEN
        data = response.json()
        assert data["code"] == ApiErrorCodeNumeric.AUTH_SPOTIFY_NOT_AUTHENTICATED
        assert data["details"]["code"] == "spotify_authorization_required"
        assert data["success"] is False

    def test_spotify_user_list_with_spotify_user_then_200_ok(self):
        self._login_as_spotify_test_user_1()
        url = self._spotify_user_list_url()

        response = self.api_client.get(url)

        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["overallTotal"] == 1
        assert len(data["results"]) == 1
        assert data["results"][0]["spotifyId"] == self.spotify_test_user_1.spotify_id

    def test_spotify_user_retrieve_then_405_method_not_allowed(self):
        self._login_as_spotify_test_user_1()
        url = self._spotify_user_detail_url(self.spotify_test_user_1.pk)

        response = self.api_client.get(url)

        assert response.status_code == status.HTTP_405_METHOD_NOT_ALLOWED

    @staticmethod
    def _spotify_user_list_url() -> str:
        from django.urls import reverse

        return reverse("spotify-user-list")

    @staticmethod
    def _spotify_user_detail_url(pk: int) -> str:
        from django.urls import reverse

        return reverse("spotify-user-detail", kwargs={"pk": pk})
