import json
from unittest.mock import MagicMock, patch

from django.test import TestCase
from rest_framework import status

from api.model.user.spotify.SpotifyUser import SpotifyUser
from api.utils.decorators.spotify import spotify_user_required
from api.view.error.ApiErrorCode import ApiErrorCodeNumeric


def _fake_view(self, request, *args, **kwargs):
    return MagicMock(status_code=200)


class TestSpotifyUserRequiredDecorator(TestCase):
    def test_unauthenticated_request_then_401_with_auth_not_authenticated(self):
        wrapped = spotify_user_required(_fake_view)
        mock_self = MagicMock()
        mock_request = MagicMock()
        mock_request.user.is_authenticated = False

        response = wrapped(mock_self, mock_request)

        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        data = json.loads(response.content)
        assert data['code'] == ApiErrorCodeNumeric.AUTH_NOT_AUTHENTICATED
        assert data['details']['code'] == 'authentication_required'
        assert data['details']['message'] == 'Authentication required to access this resource'
        assert data['success'] is False

    def test_authenticated_user_not_spotify_user_then_401_with_spotify_not_authenticated(self):
        wrapped = spotify_user_required(_fake_view)
        mock_self = MagicMock()
        mock_request = MagicMock()
        mock_request.user.is_authenticated = True
        mock_request.user.pk = 99999

        with patch.object(SpotifyUser.objects, 'get', side_effect=SpotifyUser.DoesNotExist):
            response = wrapped(mock_self, mock_request)

        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        data = json.loads(response.content)
        assert data['code'] == ApiErrorCodeNumeric.AUTH_SPOTIFY_NOT_AUTHENTICATED
        assert data['details']['code'] == 'spotify_authorization_required'
        assert data['details']['message'] == 'This resource requires Spotify authorization'
        assert data['success'] is False
