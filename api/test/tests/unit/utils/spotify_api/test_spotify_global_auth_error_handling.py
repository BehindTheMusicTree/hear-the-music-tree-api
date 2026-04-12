import json

from django.test import TestCase
from rest_framework import status

from api.exception.spotify import (
    SpotifyAuthenticationException,
    SpotifyInvalidGrantException,
    SpotifyUserNotAllowlistedException,
)
from api.view.error.ApiErrorCode import ApiErrorCodeNumeric
from api.view.error.ErrorResponse import ErrorResponse


class TestSpotifyGlobalErrorHandling(TestCase):
    def test_spotify_authentication_exception_then_401_unauthorized(self):
        exception = SpotifyAuthenticationException("Invalid Spotify credentials")
        response = ErrorResponse.handle_exception(exception)

        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        response_data = json.loads(response.content)
        assert response_data["code"] == ApiErrorCodeNumeric.AUTH_INVALID_CREDENTIALS
        assert response_data["details"]["message"] == "Invalid Spotify credentials"
        assert response_data["details"]["code"] == "spotify_authentication_error"
        assert not response_data["success"]

    def test_spotify_authentication_exception_with_empty_message_then_401_unauthorized(self):
        exception = SpotifyAuthenticationException("")
        response = ErrorResponse.handle_exception(exception)

        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        response_data = json.loads(response.content)
        assert response_data["code"] == ApiErrorCodeNumeric.AUTH_INVALID_CREDENTIALS
        assert response_data["details"]["message"] == ""
        assert response_data["details"]["code"] == "spotify_authentication_error"
        assert not response_data["success"]

    def test_spotify_authentication_exception_with_none_message_then_401_unauthorized(self):
        exception = SpotifyAuthenticationException(None)
        response = ErrorResponse.handle_exception(exception)

        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        response_data = json.loads(response.content)
        assert response_data["code"] == ApiErrorCodeNumeric.AUTH_INVALID_CREDENTIALS
        assert response_data["details"]["message"] == "None"
        assert response_data["details"]["code"] == "spotify_authentication_error"
        assert not response_data["success"]

    def test_spotify_user_not_allowlisted_exception_then_401_with_code_1007(self):
        exception = SpotifyUserNotAllowlistedException("Spotify app is in development mode.")
        response = ErrorResponse.handle_exception(exception)

        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        response_data = json.loads(response.content)
        assert response_data["code"] == ApiErrorCodeNumeric.AUTH_SPOTIFY_USER_NOT_ALLOWLISTED
        assert response_data["details"]["message"] == "Spotify app is in development mode."
        assert response_data["details"]["code"] == "spotify_user_not_allowlisted"
        assert not response_data["success"]

    def test_spotify_invalid_grant_exception_then_401_with_code_1008(self):
        exception = SpotifyInvalidGrantException(
            "Authorization code expired or already used. Please try connecting with Spotify again."
        )
        response = ErrorResponse.handle_exception(exception)

        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        response_data = json.loads(response.content)
        assert response_data["code"] == ApiErrorCodeNumeric.AUTH_SPOTIFY_CODE_EXPIRED_OR_USED
        assert response_data["details"]["code"] == "spotify_code_expired_or_used"
        assert "expired or already used" in response_data["details"]["message"]
        assert not response_data["success"]

    def test_spotify_invalid_client_then_500_internal_server_error(self):
        exception = SpotifyAuthenticationException(
            "Failed to get access token: error: invalid_client",
            detail_code="spotify_invalid_client",
        )
        response = ErrorResponse.handle_exception(exception)

        assert response.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR
        response_data = json.loads(response.content)
        assert response_data["code"] == ApiErrorCodeNumeric.SYSTEM_INTERNAL_ERROR
        assert response_data["details"]["code"] == "spotify_invalid_client"
        assert "misconfigured" in response_data["details"]["message"]
        assert not response_data["success"]
