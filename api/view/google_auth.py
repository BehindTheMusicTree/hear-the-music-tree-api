import logging

from django.conf import settings
from django.contrib.auth import login
from django.utils import timezone
from django.utils.crypto import get_random_string
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from the_music_tree_api_kit.exception.validation.app.AppValidationException import AppValidationException
from the_music_tree_api_kit.exception.validation.FieldValidationErrorCode import FieldValidationErrorCode

from api.exception.google import GoogleAuthenticationException
from api.model.user.User import User
from api.utils.google_oauth.oauth import GoogleOAuthService
from api.utils.jwt import create_jwt_token

logger = logging.getLogger(settings.APP_NAME)


class AuthRequestFields:
    CODE: str = "code"


@api_view(["POST"])
@permission_classes([AllowAny])
def google_auth(request):
    """Exchange Google code for session. One account can link both Google and Spotify (matched by email)."""
    code = request.data.get(AuthRequestFields.CODE)
    if not code:
        raise AppValidationException(
            field_name=AuthRequestFields.CODE,
            message="No code provided",
            field_validation_error_code=FieldValidationErrorCode.REQUIRED,
        )

    if not (getattr(settings, "GOOGLE_CLIENT_ID", None) or "").strip():
        return Response({"detail": "Google OAuth is not configured."}, status=status.HTTP_503_SERVICE_UNAVAILABLE)

    try:
        logger.info("Google auth: exchanging code for tokens")
        oauth_service = GoogleOAuthService()
        token_info = oauth_service.exchange_code_for_tokens(code)
        logger.info("Google auth: fetching user info")
        user_info = oauth_service.get_user_info(token_info["access_token"])
    except GoogleAuthenticationException:
        raise

    google_id = user_info["id"]
    email = user_info.get("email") or ""
    name = user_info.get("name") or user_info.get("email") or google_id
    username = name[:150] if name else str(google_id)[:150]

    user = User.objects.filter(google_id=google_id).first()
    if user:
        user.google_access_token = token_info["access_token"]
        user.google_refresh_token = token_info.get("refresh_token") or user.google_refresh_token
        user.google_profile = user_info
        user.google_token_expires_at = timezone.now() + timezone.timedelta(seconds=token_info["expires_in"])
        user.save()
    elif email:
        user = User.objects.filter(email__iexact=email).first()
        if user:
            user.google_id = google_id
            user.google_access_token = token_info["access_token"]
            user.google_refresh_token = token_info.get("refresh_token")
            user.google_profile = user_info
            user.google_token_expires_at = timezone.now() + timezone.timedelta(seconds=token_info["expires_in"])
            user.save()
        else:
            user = _create_google_user(username, email, google_id, token_info, user_info)
    else:
        user = _create_google_user(username, email or f"{google_id}@google.oauth", google_id, token_info, user_info)

    logger.info("Google auth: creating session for user id=%s", user.id)
    jwt_token = create_jwt_token(user)
    login(request, user)

    return Response(
        {
            "accessToken": jwt_token["access"],
            "refreshToken": jwt_token["refresh"],
            "expiresAt": jwt_token["expires_at_ms"],
        }
    )


def _create_google_user(username, email, google_id, token_info, user_info):
    user = User.objects.create(
        username=username,
        email=email or f"{google_id}@google.oauth",
        password=get_random_string(128),
        google_id=google_id,
        google_access_token=token_info["access_token"],
        google_refresh_token=token_info.get("refresh_token"),
        google_profile=user_info,
        google_token_expires_at=timezone.now() + timezone.timedelta(seconds=token_info["expires_in"]),
    )
    user.set_unusable_password()
    user.save()
    return user
