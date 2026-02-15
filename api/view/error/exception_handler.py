import sys

from django.http.response import Http404
from django.conf import settings
from rest_framework_simplejwt.exceptions import InvalidToken
from rest_framework.exceptions import (
    NotAuthenticated, ValidationError, MethodNotAllowed, PermissionDenied, AuthenticationFailed, ParseError,
    UnsupportedMediaType
)

from api.exception.google import GoogleAuthenticationException
from api.exception.spotify import SpotifyAuthenticationException
from api.view.error.ApiErrorCode import ApiErrorCodeNumeric
from api.view.error.ErrorResponse import ErrorResponse


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

    is_test_mode = 'pytest' in sys.argv[0]

    if settings.DEBUG and not isinstance(
        exc,
        (ValidationError, InvalidToken, NotAuthenticated, AuthenticationFailed, MethodNotAllowed, Http404,
         PermissionDenied, ParseError, UnsupportedMediaType, SpotifyAuthenticationException,
         GoogleAuthenticationException)):
        if is_test_mode:
            return _handle_exception_with_request(exc, context)
        return None

    return _handle_exception_with_request(exc, context)


def _handle_exception_with_request(exc, context):
    request = None
    if context:
        request = context.get('request')
        if request is None and context.get('view') is not None:
            request = getattr(context['view'], 'request', None)
    is_authenticated = False
    if request is not None and getattr(request, 'user', None) is not None:
        is_authenticated = bool(getattr(request.user, 'is_authenticated', False))
    if isinstance(exc, PermissionDenied) and not is_authenticated:
        return ErrorResponse.create_error_response(
            error_detail={'message': 'Authentication required', 'code': 'authentication_required'},
            api_error_code=ApiErrorCodeNumeric.AUTH_NOT_AUTHENTICATED
        )
    return ErrorResponse.handle_exception(exc)
