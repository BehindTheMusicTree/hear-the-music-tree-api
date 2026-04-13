"""Exception classes for Spotify API integration"""


class SpotifyException(Exception):
    """Base exception for all Spotify-related exceptions"""


class SpotifyAuthenticationException(SpotifyException):
    """Exception raised when authentication with Spotify fails."""

    def __init__(self, message: str, *, detail_code: str | None = None):
        super().__init__(message)
        self.detail_code = detail_code or "spotify_authentication_error"


class SpotifyUserNotAllowlistedException(SpotifyAuthenticationException):
    """Exception raised when Spotify returns 403 because the user is not in the app's User Management (development
    mode).
    """


class SpotifyInvalidGrantException(SpotifyAuthenticationException):
    """Exception raised when Spotify returns invalid_grant (e.g. authorization code expired or already used)."""


class SpotifyResourceNotFoundException(SpotifyException):
    """Exception raised when a requested resource is not found on Spotify"""


class SpotifyRateLimitException(SpotifyException):
    """Exception raised when Spotify API rate limit is exceeded"""


class SpotifyNetworkException(SpotifyException):
    """Exception raised when there's a network error communicating with Spotify"""


class SpotifyAPIException(SpotifyException):
    """Exception raised for general Spotify API errors"""


class SpotifyForbiddenException(SpotifyException):
    """Exception raised when access to a resource is forbidden"""
