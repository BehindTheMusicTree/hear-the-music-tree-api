from unittest import mock

from django.urls import reverse
from rest_framework import status

from api.model.user.User import User
from api.test.utils.AppTestCase import AppTestCase
from api.view.google_auth import AuthRequestFields


class TestGoogleAuthView(AppTestCase):
    def test_missing_code_then_400_bad_request(self):
        response = self.api_client.post(
            reverse("api-auth-google"),
            data={},
            content_type="application/json",
        )
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_empty_code_then_400_bad_request(self):
        response = self.api_client.post(
            reverse("api-auth-google"),
            data={AuthRequestFields.CODE: ""},
            content_type="application/json",
        )
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    @mock.patch("api.view.google_auth.GoogleOAuthService")
    def test_invalid_code_then_401_unauthorized(self, mock_service_class):
        from api.exception.google import GoogleAuthenticationException

        mock_service = mock_service_class.return_value
        mock_service.exchange_code_for_tokens.side_effect = GoogleAuthenticationException("Invalid code")

        response = self.api_client.post(
            reverse("api-auth-google"),
            data={AuthRequestFields.CODE: "invalid_code"},
            content_type="application/json",
        )
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    @mock.patch("api.view.google_auth.GoogleOAuthService")
    def test_valid_code_then_200_and_session_shape(self, mock_service_class):
        mock_service = mock_service_class.return_value
        mock_service.exchange_code_for_tokens.return_value = {
            "access_token": "google_access_123",
            "refresh_token": "google_refresh_123",
            "expires_in": 3600,
            "id_token": None,
        }
        mock_service.get_user_info.return_value = {
            "id": "google_user_456",
            "email": "google@example.com",
            "name": "Google User",
        }

        response = self.api_client.post(
            reverse("api-auth-google"),
            data={AuthRequestFields.CODE: "valid_authorization_code"},
            content_type="application/json",
        )

        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert "accessToken" in data
        assert "refreshToken" in data
        assert "expiresAt" in data
        assert isinstance(data["expiresAt"], (int, float))

        user = User.objects.get(google_id="google_user_456")
        assert user.email == "google@example.com"
        assert user.google_access_token == "google_access_123"
        assert user.google_profile["name"] == "Google User"
