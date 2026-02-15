from unittest import mock

import requests

from api.exception.google import GoogleAuthenticationException
from api.test.utils.AppTestCase import AppTestCase
from api.utils.google_oauth.oauth import GoogleOAuthService


class TestGoogleOAuthAuth(AppTestCase):
    @mock.patch('api.utils.google_oauth.oauth.requests.post')
    def test_exchange_code_with_valid_code_then_returns_tokens(self, mock_post):
        mock_post.return_value.raise_for_status = mock.Mock()
        mock_post.return_value.json.return_value = {
            "access_token": "test_access_token",
            "refresh_token": "test_refresh_token",
            "expires_in": 3600,
        }

        service = GoogleOAuthService()
        tokens = service.exchange_code_for_tokens("valid_code")

        assert tokens["access_token"] == "test_access_token"
        assert tokens["refresh_token"] == "test_refresh_token"
        assert tokens["expires_in"] == 3600
        mock_post.assert_called_once()

    @mock.patch('api.utils.google_oauth.oauth.requests.post')
    def test_exchange_code_with_invalid_code_then_raises_exception(self, mock_post):
        mock_response = mock.Mock()
        mock_response.json.return_value = {"error": "invalid_grant", "error_description": "Bad request"}
        mock_post.return_value.raise_for_status.side_effect = requests.HTTPError(response=mock_response)

        service = GoogleOAuthService()
        with self.assertRaises(GoogleAuthenticationException) as context:
            service.exchange_code_for_tokens("invalid_code")
        assert "Failed to exchange code" in str(context.exception)

    @mock.patch('api.utils.google_oauth.oauth.requests.get')
    def test_get_user_info_with_valid_token_then_returns_user_info(self, mock_get):
        mock_get.return_value.raise_for_status = mock.Mock()
        mock_get.return_value.json.return_value = {
            "id": "google_123",
            "email": "user@example.com",
            "name": "Test User",
        }

        service = GoogleOAuthService()
        user_info = service.get_user_info("valid_token")

        assert user_info["id"] == "google_123"
        assert user_info["email"] == "user@example.com"
        assert user_info["name"] == "Test User"
        mock_get.assert_called_once()

    @mock.patch('api.utils.google_oauth.oauth.requests.get')
    def test_get_user_info_with_invalid_token_then_raises_exception(self, mock_get):
        mock_response = mock.Mock()
        mock_response.json.return_value = {"error": "invalid_token"}
        mock_get.return_value.raise_for_status.side_effect = requests.HTTPError(response=mock_response)

        service = GoogleOAuthService()
        with self.assertRaises(GoogleAuthenticationException) as context:
            service.get_user_info("invalid_token")
        assert "Failed to get user info" in str(context.exception)
