from unittest import mock

from spotipy.exceptions import SpotifyException as SpotipyException

from api.exception.spotify import SpotifyAuthenticationException
from api.model.user.User import User
from api.model.user.spotify.Fields import Fields
from api.test.utils.AppTestCase import AppTestCase
from api.utils.spotify_api.oauth import SpotifyOAuthService


class TestSpotifyProfile(AppTestCase):
    def setUp(self):
        super().setUp()
        self.test_user1 = User(username='spotify_user1', email='spotify@user1.com',
                              spotify_id='spotify_user1_id', is_test_user=True)
        self.test_user1.set_password('spotify_user1')
        self.test_user1.save()
        self.test_user2 = User(username='spotify_user2', email='spotify@user2.com',
                              spotify_id='spotify_user2_id', is_test_user=True)
        self.test_user2.set_password('spotify_user2')
        self.test_user2.save()
        self._login_as_test_user1()

    @mock.patch('api.utils.spotify_api.oauth.spotipy.Spotify')
    def test_get_user_info_with_valid_token_then_returns_complete_profile(self, mock_spotify):
        mock_spotify.return_value.current_user.return_value = {
            Fields.ID: "test_user",
            Fields.EMAIL: "test@example.com",
            Fields.DISPLAY_NAME: "Test User",
            Fields.COUNTRY: "US",
            Fields.PRODUCT: "premium",
            Fields.IMAGES: [{Fields.URL: "https://example.com/image.jpg"}]
        }

        service = SpotifyOAuthService()
        user_info = service.get_user_info("valid_token")

        assert user_info[Fields.ID] == "test_user"
        assert user_info[Fields.EMAIL] == "test@example.com"
        assert user_info[Fields.DISPLAY_NAME] == "Test User"
        assert user_info[Fields.COUNTRY] == "US"
        assert user_info[Fields.PRODUCT] == "premium"
        assert len(user_info[Fields.IMAGES]) == 1
        assert user_info[Fields.IMAGES][0][Fields.URL] == "https://example.com/image.jpg"
        mock_spotify.return_value.current_user.assert_called_once()

    @mock.patch('api.utils.spotify_api.oauth.spotipy.Spotify')
    def test_get_user_info_with_minimal_profile_then_returns_basic_fields(self, mock_spotify):
        mock_spotify.return_value.current_user.return_value = {
            Fields.ID: "test_user",
            Fields.DISPLAY_NAME: "Test User"
        }

        service = SpotifyOAuthService()
        user_info = service.get_user_info("valid_token")

        assert user_info[Fields.ID] == "test_user"
        assert user_info[Fields.DISPLAY_NAME] == "Test User"
        assert Fields.EMAIL not in user_info
        assert Fields.COUNTRY not in user_info
        assert Fields.PRODUCT not in user_info
        assert Fields.IMAGES not in user_info
        mock_spotify.return_value.current_user.assert_called_once()

    @mock.patch('api.utils.spotify_api.oauth.spotipy.Spotify')
    def test_get_user_info_with_invalid_token_then_raises_exception(self, mock_spotify):
        mock_spotify.return_value.current_user.side_effect = Exception("Invalid token")

        service = SpotifyOAuthService()
        with self.assertRaises(SpotifyAuthenticationException) as context:
            service.get_user_info("invalid_token")
        assert "Failed to get user info" in str(context.exception)

    @mock.patch('api.utils.spotify_api.oauth.spotipy.Spotify')
    def test_get_user_info_with_network_error_then_raises_exception(self, mock_spotify):
        mock_spotify.return_value.current_user.side_effect = Exception("Network error")

        service = SpotifyOAuthService()
        with self.assertRaises(SpotifyAuthenticationException) as context:
            service.get_user_info("valid_token")
        assert "Failed to get user info" in str(context.exception)

    @mock.patch('api.utils.spotify_api.oauth.spotipy.Spotify')
    def test_get_user_info_with_403_allowlist_message_then_raises_with_allowlist_detail_code(self, mock_spotify):
        mock_spotify.return_value.current_user.side_effect = SpotipyException(
            403,
            -1,
            "https://api.spotify.com/v1/me:\n Check settings on developer.spotify.com/dashboard, the user may not be registered.",
            reason=None,
        )

        service = SpotifyOAuthService()
        with self.assertRaises(SpotifyAuthenticationException) as context:
            service.get_user_info("token")
        assert getattr(context.exception, "detail_code", None) == "spotify_user_not_in_allowlist"
        assert "add you in the Spotify Developer Dashboard" in str(context.exception)

    @mock.patch('api.utils.spotify_api.oauth.spotipy.Spotify')
    def test_get_user_info_with_403_without_allowlist_message_then_raises_generic(self, mock_spotify):
        mock_spotify.return_value.current_user.side_effect = SpotipyException(
            403,
            -1,
            "Forbidden: app restricted",
            reason=None,
        )

        service = SpotifyOAuthService()
        with self.assertRaises(SpotifyAuthenticationException) as context:
            service.get_user_info("token")
        assert getattr(context.exception, "detail_code", None) != "spotify_user_not_in_allowlist"
        assert "app restricted" in str(context.exception)
