"""
Exception classes for Spotify API integration
"""


class SpotifyException(Exception):
    """Base exception for all Spotify-related exceptions"""
    pass


class SpotifyAuthenticationException(SpotifyException):
    """Exception raised when authentication with Spotify fails"""
    pass


class SpotifyUserNotAllowlistedException(SpotifyAuthenticationException):
    """Exception raised when Spotify returns 403 because the user is not in the app's User Management (development mode)."""
    pass


class SpotifyResourceNotFoundException(SpotifyException):
    """Exception raised when a requested resource is not found on Spotify"""
    pass


class SpotifyRateLimitException(SpotifyException):
    """Exception raised when Spotify API rate limit is exceeded"""
    pass


class SpotifyNetworkException(SpotifyException):
    """Exception raised when there's a network error communicating with Spotify"""
    pass


class SpotifyAPIException(SpotifyException):
    """Exception raised for general Spotify API errors"""
    pass


class SpotifyForbiddenException(SpotifyException):
    """Exception raised when access to a resource is forbidden"""
    pass
