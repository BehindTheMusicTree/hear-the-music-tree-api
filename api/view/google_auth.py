from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from django.utils import timezone
from django.utils.crypto import get_random_string
from django.contrib.auth import login

from api.utils.google_oauth.oauth import GoogleOAuthService
from api.utils.jwt import create_jwt_token
from api.model.user.google.GoogleUser import GoogleUser
from api.model.user.google.Fields import Fields as GoogleUserFields
from api.exception.validation.app.AppValidationException import AppValidationException
from api.exception.validation.FieldValidationErrorCode import FieldValidationErrorCode
from api.exception.google import GoogleAuthenticationException


class AuthRequestFields:
    CODE: str = "code"


@api_view(['POST'])
@permission_classes([AllowAny])
def google_auth(request):
    """
    Exchange Google OAuth authorization code for session tokens.
    Request body: { "code": "<authorization_code_from_google_callback>" }
    Response: { accessToken, refreshToken, expiresAt } (same shape as Spotify auth).
    """
    code = request.data.get(AuthRequestFields.CODE)
    if not code:
        raise AppValidationException(
            field_name=AuthRequestFields.CODE,
            message="No code provided",
            field_validation_error_code=FieldValidationErrorCode.REQUIRED,
        )

    try:
        oauth_service = GoogleOAuthService()
        token_info = oauth_service.exchange_code_for_tokens(code)
        user_info = oauth_service.get_user_info(token_info["access_token"])
    except GoogleAuthenticationException:
        raise

    google_id = user_info["id"]
    email = user_info.get("email") or ""
    name = user_info.get("name") or user_info.get("email") or google_id
    username = name[:150] if name else str(google_id)[:150]

    user, created = GoogleUser.objects.get_or_create(
        google_id=google_id,
        defaults={
            GoogleUserFields.EMAIL: email or f"{google_id}@google.oauth",
            GoogleUserFields.USERNAME: username,
            GoogleUserFields.PASSWORD: get_random_string(128),
            GoogleUserFields.GOOGLE_ACCESS_TOKEN: token_info["access_token"],
            GoogleUserFields.GOOGLE_REFRESH_TOKEN: token_info.get("refresh_token"),
            GoogleUserFields.GOOGLE_PROFILE: user_info,
            GoogleUserFields.GOOGLE_TOKEN_EXPIRES_AT: timezone.now()
            + timezone.timedelta(seconds=token_info["expires_in"]),
        },
    )
    if created:
        user.set_unusable_password()
        user.save()
    else:
        user.google_access_token = token_info["access_token"]
        user.google_refresh_token = token_info.get("refresh_token") or user.google_refresh_token
        user.google_profile = user_info
        user.google_token_expires_at = timezone.now() + timezone.timedelta(
            seconds=token_info["expires_in"]
        )
        user.save()

    jwt_token = create_jwt_token(user)
    login(request, user)

    return Response({
        "accessToken": jwt_token["access"],
        "refreshToken": jwt_token["refresh"],
        "expiresAt": jwt_token["expires_at_ms"],
    })
