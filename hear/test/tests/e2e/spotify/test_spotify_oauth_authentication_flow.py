from unittest import mock

import pytest
from django.urls import reverse
from rest_framework import status
from the_music_tree_api_kit.utils.data_transformer import to_camel_case
from the_music_tree_api_kit.view.error.ApiErrorCode import ApiErrorCodeNumeric

from hear.exception.spotify import SpotifyInvalidGrantException
from hear.model.user.spotify.Fields import Fields as SpotifyUserFields
from hear.model.user.User import User
from hear.serializer.token.Fields import Fields as TokenFields
from hear.test.utils.AppTestCase import AppTestCase


@pytest.mark.e2e
class TestCase(AppTestCase):
    """
    E2E test for complete Spotify OAuth authentication flow.

    This test verifies the complete workflow:
    1. User initiates Spotify OAuth flow
    2. User authorizes application on Spotify
    3. System receives authorization code
    4. System exchanges code for Spotify access/refresh tokens
    5. System creates/updates Spotify user account
    6. System returns JWT tokens for API authentication
    7. User uses JWT token to access API

    Note: This test uses mocks for Spotify (OAuth + API). For real E2E testing,
    set SPOTIFY_ENABLED=true and configure actual Spotify credentials. In CI,
    conftest mocks Spotify; this test overrides with its own mock so the flow is deterministic.
    """

    @mock.patch("hear.view.spotify_auth.SpotifyOAuthService")
    def test_spotify_oauth_authentication_flow_then_ok(self, mock_oauth_class):
        authorization_code = "test_authorization_code"
        spotify_id = "test_spotify_user_id"
        email = "test@example.com"
        display_name = "Test User"

        mock_service = mock_oauth_class.return_value
        mock_service.get_access_token.return_value = {
            TokenFields.ACCESS_TOKEN: "test_access_token",
            TokenFields.REFRESH_TOKEN: "test_refresh_token",
            TokenFields.EXPIRES_IN: 3600,
        }
        mock_service.get_user_info.return_value = {
            SpotifyUserFields.ID: spotify_id,
            SpotifyUserFields.EMAIL: email,
            SpotifyUserFields.DISPLAY_NAME: display_name,
            SpotifyUserFields.FOLLOWERS: {"total": 100},
            SpotifyUserFields.IMAGES: [{"url": "https://example.com/image.jpg"}],
            SpotifyUserFields.URI: f"spotify:user:{spotify_id}",
            SpotifyUserFields.HREF: f"https://api.spotify.com/v1/users/{spotify_id}",
            SpotifyUserFields.TYPE: "user",
        }

        response = self.api_client.post(
            reverse("api-auth-spotify"), data={"code": authorization_code}, content_type="application/json"
        )

        assert response.status_code == status.HTTP_200_OK
        response_data = response.json()

        assert to_camel_case(TokenFields.ACCESS_TOKEN) in response_data
        assert to_camel_case(TokenFields.REFRESH_TOKEN) in response_data
        assert "expiresAt" in response_data
        assert "spotifyUser" in response_data

        spotify_user_data = response_data["spotifyUser"]
        assert spotify_user_data[to_camel_case(SpotifyUserFields.ID)] is not None
        assert spotify_user_data[to_camel_case(SpotifyUserFields.EMAIL)] == email
        assert spotify_user_data[to_camel_case(SpotifyUserFields.DISPLAY_NAME)] == display_name

        user = User.objects.get(spotify_id=spotify_id)
        assert user is not None
        assert user.email == email
        assert user.spotify_id == spotify_id
        assert user.spotify_access_token == "test_access_token"
        assert user.spotify_refresh_token == "test_refresh_token"

        access_token = response_data[to_camel_case(TokenFields.ACCESS_TOKEN)]
        self.api_client.credentials(HTTP_AUTHORIZATION=f"Bearer {access_token}")

        response = self.api_client.get(reverse("me-playlist-list"))
        assert response.status_code == status.HTTP_200_OK

    @mock.patch("hear.view.spotify_auth.SpotifyOAuthService")
    def test_post_auth_spotify_when_invalid_grant_then_401_with_code_1008(self, mock_oauth_class):
        mock_oauth_class.return_value.get_access_token.side_effect = SpotifyInvalidGrantException(
            "Authorization code expired or already used. Please try connecting with Spotify again."
        )

        response = self.api_client.post(
            reverse("api-auth-spotify"),
            data={"code": "expired_or_used_code"},
            content_type="application/json",
        )

        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        data = response.json()
        assert data["code"] == ApiErrorCodeNumeric.AUTH_SPOTIFY_CODE_EXPIRED_OR_USED
        assert data["details"]["code"] == "spotify_code_expired_or_used"
        assert "expired or already used" in data["details"]["message"]
        assert data["success"] is False
