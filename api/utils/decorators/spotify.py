from functools import wraps

from api.view.error.ApiErrorCode import ApiErrorCodeNumeric
from api.view.error.ErrorResponse import ErrorResponse


def spotify_user_required(view_func):
    """Decorator for view methods that require the current user to have Spotify linked."""

    @wraps(view_func)
    def wrapper(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return ErrorResponse.create_error_response(
                error_detail={
                    "message": "Authentication required to access this resource",
                    "code": "authentication_required",
                },
                api_error_code=ApiErrorCodeNumeric.AUTH_NOT_AUTHENTICATED,
            )

        if not getattr(request.user, "spotify_id", None):
            return ErrorResponse.create_error_response(
                error_detail={
                    "message": "This resource requires Spotify authorization",
                    "code": "spotify_authorization_required",
                },
                api_error_code=ApiErrorCodeNumeric.AUTH_SPOTIFY_NOT_AUTHENTICATED,
            )

        return view_func(self, request, *args, **kwargs)

    return wrapper
