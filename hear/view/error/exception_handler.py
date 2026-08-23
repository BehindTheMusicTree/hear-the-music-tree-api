import logging
import sys

from django.conf import settings
from rest_framework.exceptions import AuthenticationFailed, NotAuthenticated, PermissionDenied
from rest_framework_simplejwt.exceptions import InvalidToken
from the_music_tree_api_kit.view.error.ApiErrorCode import ApiErrorCodeNumeric
from the_music_tree_api_kit.view.error.ErrorResponse import ErrorResponse
from the_music_tree_api_kit.view.error.ErrorResponseFields import ErrorResponseFields

from hear.exception.google import GoogleAuthenticationException
from hear.exception.spotify import (
    SpotifyAuthenticationException,
    SpotifyInvalidGrantException,
    SpotifyUserNotAllowlistedException,
)


def _from_invalid_jwt_token(exception: InvalidToken | NotAuthenticated | AuthenticationFailed):
    try:
        detail = exception.detail
        message = detail["detail"] if isinstance(detail, dict) and "detail" in detail else exception.default_detail
        code = detail["code"] if isinstance(detail, dict) and "code" in detail else exception.default_code
    except AttributeError, TypeError:
        message = getattr(exception, "default_detail", str(exception))
        code = getattr(exception, "default_code", "authentication_failed")
    api_error_code = (
        ApiErrorCodeNumeric.AUTH_NOT_AUTHENTICATED
        if code == "authentication_required"
        else ApiErrorCodeNumeric.AUTH_INVALID_CREDENTIALS
    )
    return ErrorResponse.create_error_response(
        error_detail={"message": message, "code": code}, api_error_code=api_error_code
    )


def _from_spotify_user_not_allowlisted_exception(exception: SpotifyUserNotAllowlistedException):
    try:
        message = str(exception)
    except Exception:
        message = ErrorResponseFields.MESSAGES[ApiErrorCodeNumeric.AUTH_SPOTIFY_USER_NOT_ALLOWLISTED]
    return ErrorResponse.create_error_response(
        error_detail={"message": message, "code": "spotify_user_not_allowlisted"},
        api_error_code=ApiErrorCodeNumeric.AUTH_SPOTIFY_USER_NOT_ALLOWLISTED,
    )


def _from_spotify_invalid_grant_exception(exception: SpotifyInvalidGrantException):
    try:
        message = str(exception)
    except Exception:
        message = ErrorResponseFields.MESSAGES[ApiErrorCodeNumeric.AUTH_SPOTIFY_CODE_EXPIRED_OR_USED]
    return ErrorResponse.create_error_response(
        error_detail={"message": message, "code": "spotify_code_expired_or_used"},
        api_error_code=ApiErrorCodeNumeric.AUTH_SPOTIFY_CODE_EXPIRED_OR_USED,
    )


def _from_spotify_authentication_exception(exception: SpotifyAuthenticationException):
    detail_code = getattr(exception, "detail_code", "spotify_authentication_error")
    if detail_code == "spotify_invalid_client":
        return ErrorResponse.create_error_response(
            error_detail={
                "message": "Sign-in is temporarily misconfigured. Please try again later or contact support.",
                "code": detail_code,
            },
            api_error_code=ApiErrorCodeNumeric.SYSTEM_INTERNAL_ERROR,
        )
    try:
        message = str(exception)
    except Exception:
        message = f"{type(exception).__name__}: <unable to stringify exception>"
    return ErrorResponse.create_error_response(
        error_detail={"message": message, "code": detail_code},
        api_error_code=ApiErrorCodeNumeric.AUTH_INVALID_CREDENTIALS,
    )


def _from_google_authentication_exception(exception: GoogleAuthenticationException):
    try:
        message = str(exception)
    except Exception:
        message = f"{type(exception).__name__}: <unable to stringify exception>"
    detail_code = getattr(exception, "detail_code", "google_authentication_error")
    if detail_code in (
        "google_oauth_redirect_uri_mismatch",
        "google_oauth_invalid_client",
        "google_oauth_unauthorized_client",
    ):
        return ErrorResponse.create_error_response(
            error_detail={
                "message": "Sign-in is temporarily misconfigured. Please try again later or contact support.",
                "code": detail_code,
            },
            api_error_code=ApiErrorCodeNumeric.SYSTEM_INTERNAL_ERROR,
        )
    return ErrorResponse.create_error_response(
        error_detail={"message": message, "code": detail_code},
        api_error_code=ApiErrorCodeNumeric.AUTH_INVALID_CREDENTIALS,
    )


ErrorResponse.register_handler(InvalidToken, _from_invalid_jwt_token)
ErrorResponse.register_handler(SpotifyUserNotAllowlistedException, _from_spotify_user_not_allowlisted_exception)
ErrorResponse.register_handler(SpotifyInvalidGrantException, _from_spotify_invalid_grant_exception)
ErrorResponse.register_handler(SpotifyAuthenticationException, _from_spotify_authentication_exception)
ErrorResponse.register_handler(GoogleAuthenticationException, _from_google_authentication_exception)


def custom_exception_handler(exc, context):
    """
    Custom exception handler for DRF that integrates with our ErrorResponse system.
    In debug mode, it falls back to Django's default HTML traceback.
    In production, it uses our custom error response format.
    In test mode, it always returns JSON responses to avoid Django's debug error page rendering.

    Important Note on Middleware Exceptions:
    --------------------------------------
    This handler only processes exceptions from DRF views and viewsets. Exceptions raised
    in middleware are handled differently because they occur before reaching DRF's
    exception handling system.

    For middleware exceptions:
    1. Do not raise exceptions in middleware expecting them to be caught here
    2. Instead, handle exceptions directly in the middleware using ErrorResponse
    3. Return a JsonResponse instead of raising

    Example middleware pattern:
        class YourMiddleware:
            def handle_error(self, exc):
                return ErrorResponse.handle_exception(exc)

            def __call__(self, request):
                if error_condition:
                    return self.handle_error(SomeException("error message"))
                return self.get_response(request)

    This ensures consistent error handling and formatting across the application,
    whether the error occurs in middleware or views.

    Args:
        exc: The caught exception
        context: Additional context (includes the request)

    Returns:
        Response object with error details in production and tests,
        None in debug mode (non-test) to let Django's default handler show the traceback page
    """

    is_test_mode = "pytest" in sys.argv[0]

    if settings.DEBUG and not isinstance(exc, ErrorResponse.get_registered_exception_types()):
        if is_test_mode:
            return _handle_exception_with_request(exc, context)
        return None

    return _handle_exception_with_request(exc, context)


def _handle_exception_with_request(exc, context):
    request = None
    if context:
        request = context.get("request")
        if request is None and context.get("view") is not None:
            request = getattr(context["view"], "request", None)
    is_authenticated = False
    if request is not None and getattr(request, "user", None) is not None:
        is_authenticated = bool(getattr(request.user, "is_authenticated", False))
    if isinstance(exc, PermissionDenied) and not is_authenticated:
        return ErrorResponse.create_error_response(
            error_detail={"message": "Authentication required", "code": "authentication_required"},
            api_error_code=ApiErrorCodeNumeric.AUTH_NOT_AUTHENTICATED,
        )
    logging.getLogger("exceptions").exception("Exception handled by DRF exception handler", exc_info=exc)
    return ErrorResponse.handle_exception(exc)
