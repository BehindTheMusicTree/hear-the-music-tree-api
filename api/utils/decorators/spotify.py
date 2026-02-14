from functools import wraps

from api.model.user.spotify.SpotifyUser import SpotifyUser
from api.view.error.ApiErrorCode import ApiErrorCodeNumeric
from api.view.error.ErrorResponse import ErrorResponse


def spotify_user_required(view_func):
    """
    Decorator for view methods that require a SpotifyUser.

    This decorator:
    1. Checks if the request.user is authenticated
    2. Attempts to retrieve the matching SpotifyUser
    3. Casts request.user to SpotifyUser for the view function's use

    Usage:
        @spotify_user_required
        def view_method(self, request, ...):
            # request.user is guaranteed to be a SpotifyUser here
    """
    @wraps(view_func)
    def wrapper(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return ErrorResponse.create_error_response(
                error_detail={'message': 'Authentication required to access this resource', 'code': 'authentication_required'},
                api_error_code=ApiErrorCodeNumeric.AUTH_NOT_AUTHENTICATED
            )

        try:
            spotify_user = SpotifyUser.objects.get(pk=request.user.pk)
            request.user = spotify_user
        except SpotifyUser.DoesNotExist:
            return ErrorResponse.create_error_response(
                error_detail={'message': 'This resource requires Spotify authorization', 'code': 'spotify_authorization_required'},
                api_error_code=ApiErrorCodeNumeric.AUTH_SPOTIFY_NOT_AUTHENTICATED
            )

        return view_func(self, request, *args, **kwargs)

    return wrapper
