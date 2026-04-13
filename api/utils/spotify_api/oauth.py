import logging
from typing import Optional, TypedDict

import spotipy
from django.conf import settings
from spotipy.exceptions import SpotifyException as SpotipyException
from spotipy.oauth2 import SpotifyOAuth

from api.exception import spotify as spotify_exception
from api.exception.spotify import (
    SpotifyInvalidGrantException,
    SpotifyUserNotAllowlistedException,
)

logger = logging.getLogger(settings.APP_NAME)


class TokenInfo(TypedDict):
    access_token: str
    refresh_token: str
    expires_in: int


class SpotifyOAuthService:
    """Service class for handling Spotify OAuth authentication"""

    def __init__(self):
        """Initialize with Spotify OAuth configuration"""
        self.oauth = SpotifyOAuth(
            client_id=settings.SPOTIFY_CLIENT_ID,
            client_secret=settings.SPOTIFY_CLIENT_SECRET,
            redirect_uri=settings.SPOTIFY_REDIRECT_URI,
            scope=settings.SPOTIFY_SCOPES,
        )

    def get_auth_url(self, state: str | None = None) -> str:
        """
        Get the Spotify authorization URL

        Args:
            state: Optional state parameter for CSRF protection

        Returns:
            The authorization URL
        """
        return self.oauth.get_authorize_url(state=state)

    def get_access_token(self, code: str) -> TokenInfo:
        """
        Exchange authorization code for access token.

        Uses check_cache=False so each login uses the provided code instead of
        spotipy's default file cache, which would otherwise return the first
        cached user's token for every request.
        """
        try:
            token_info = self.oauth.get_access_token(code, check_cache=False)
            if token_info is None:
                raise spotify_exception.SpotifyAuthenticationException(
                    "Failed to get access token: No token info returned"
                )
            return token_info
        except Exception as e:
            err_str = str(e)
            logger.error(f"Failed to get access token: {err_str}")
            if (
                "invalid_grant" in err_str.lower()
                or "invalid authorization code" in err_str.lower()
                or "authorization code expired" in err_str.lower()
            ):
                raise SpotifyInvalidGrantException(
                    "Authorization code expired or already used. Please try connecting with Spotify again."
                )
            detail_code = "spotify_invalid_client" if "invalid_client" in err_str.lower() else None
            raise spotify_exception.SpotifyAuthenticationException(
                f"Failed to get access token: {err_str}", detail_code=detail_code
            )

    def refresh_access_token(self, refresh_token: str) -> TokenInfo:
        """
        Refresh an expired access token

        Args:
            refresh_token: The refresh token

        Returns:
            Dictionary containing new access token
        """
        try:
            token_info = self.oauth.refresh_access_token(refresh_token)
            if token_info is None:
                raise spotify_exception.SpotifyAuthenticationException(
                    "Failed to refresh access token: No token info returned"
                )
            return token_info
        except Exception as e:
            logger.error(f"Failed to refresh access token: {e!s}")
            detail_code = "spotify_invalid_client" if "invalid_client" in str(e).lower() else None
            raise spotify_exception.SpotifyAuthenticationException(
                f"Failed to refresh access token: {e!s}", detail_code=detail_code
            )

    _SPOTIFY_DEV_MODE_MESSAGE = (
        "Spotify app is in development mode. Your account must be added in the "
        "Spotify Developer Dashboard (Users and Access) to sign in."
    )

    def get_user_info(self, access_token: str) -> dict:
        """
        Get user information from Spotify

        Args:
            access_token: The access token

        Returns:
            Dictionary containing user information
        """
        try:
            sp = spotipy.Spotify(auth=access_token)
            user_info = sp.current_user()
            if user_info is None:
                raise spotify_exception.SpotifyAuthenticationException("Failed to get user info: No user info returned")
            return user_info
        except SpotipyException as e:
            logger.error("Failed to get user info: %s", str(e))
            allowlist_phrases = ("user may not be registered", "developer.spotify.com/dashboard")
            msg_lower = (e.msg or "").lower()
            if e.http_status == 403 and any(phrase in msg_lower for phrase in allowlist_phrases):
                raise spotify_exception.SpotifyAuthenticationException(
                    "Your Spotify account is not authorized for this app. The app owner must add you in the Spotify Developer Dashboard (User Management).",
                    detail_code="spotify_user_not_in_allowlist",
                ) from e
            raise spotify_exception.SpotifyAuthenticationException(f"Failed to get user info: {e.msg or str(e)}") from e
        except Exception as e:
            err_str = str(e)
            logger.error("Failed to get user info: %s", err_str)
            if "403" in err_str and ("user may not be registered" in err_str or "developer.spotify.com" in err_str):
                raise SpotifyUserNotAllowlistedException(self._SPOTIFY_DEV_MODE_MESSAGE) from e
            raise spotify_exception.SpotifyAuthenticationException(f"Failed to get user info: {err_str}") from e
