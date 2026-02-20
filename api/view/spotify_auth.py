from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from django.utils import timezone
from django.utils.crypto import get_random_string
from django.contrib.auth import login

from api.utils.spotify_api.oauth import SpotifyOAuthService
from api.utils.jwt import create_jwt_token
from api.model.user.User import User
from api.model.user.Fields import Fields as UserFields
from api.model.spotify_resource.Fields import Fields as SpotifyFields
from api.exception.validation.app.AppValidationException import AppValidationException
from api.exception.validation.FieldValidationErrorCode import FieldValidationErrorCode


class SpotifyProfileFields:
    DISPLAY_NAME = "display_name"
    FOLLOWERS = "followers"
    HREF = "href"
    IMAGES = "images"
    TYPE = "type"
    URI = "uri"


@api_view(['POST'])
@permission_classes([AllowAny])
def spotify_auth(request):
    """
    Exchange Spotify code for session. One account can link both Spotify and Google (matched by email).
    """
    code = request.data.get('code')
    if not code:
        raise AppValidationException(
            field_name='code',
            message='No code provided',
            field_validation_error_code=FieldValidationErrorCode.REQUIRED
        )

    oauth_service = SpotifyOAuthService()
    token_info = oauth_service.get_access_token(code)
    access_token = token_info['access_token']
    refresh_token = token_info['refresh_token']
    user_info = oauth_service.get_user_info(access_token)

    spotify_id = user_info['id']
    email = user_info.get('email')
    display_name = user_info.get('display_name', spotify_id)
    username = (display_name or spotify_id)[:150]

    user = User.objects.filter(spotify_id=spotify_id).first()
    if user:
        user.spotify_access_token = access_token
        user.spotify_refresh_token = refresh_token
        user.spotify_profile = user_info
        user.spotify_token_expires_at = timezone.now() + timezone.timedelta(seconds=token_info['expires_in'])
        user.save()
    elif email:
        user = User.objects.filter(email__iexact=email).first()
        if user:
            user.spotify_id = spotify_id
            user.spotify_access_token = access_token
            user.spotify_refresh_token = refresh_token
            user.spotify_profile = user_info
            user.spotify_token_expires_at = timezone.now() + timezone.timedelta(seconds=token_info['expires_in'])
            user.save()
        else:
            user = User.objects.create(
                username=username,
                email=email or f"{spotify_id}@spotify.oauth",
                password=get_random_string(128),
                spotify_id=spotify_id,
                spotify_access_token=access_token,
                spotify_refresh_token=refresh_token,
                spotify_profile=user_info,
                spotify_token_expires_at=timezone.now() + timezone.timedelta(seconds=token_info['expires_in']),
            )
            user.set_unusable_password()
            user.save()
    else:
        user = User.objects.create(
            username=username,
            email=email or f"{spotify_id}@spotify.oauth",
            password=get_random_string(128),
            spotify_id=spotify_id,
            spotify_access_token=access_token,
            spotify_refresh_token=refresh_token,
            spotify_profile=user_info,
            spotify_token_expires_at=timezone.now() + timezone.timedelta(seconds=token_info['expires_in']),
        )
        user.set_unusable_password()
        user.save()

    jwt_token = create_jwt_token(user)
    login(request, user)

    profile = user.spotify_profile or {}
    return Response({
        'accessToken': jwt_token['access'],
        'refreshToken': jwt_token['refresh'],
        'expiresAt': jwt_token['expires_at_ms'],
        'spotifyUser': {
            UserFields.SPOTIFY_PROFILE: user.spotify_profile,
            UserFields.ID: user.id,
            UserFields.EMAIL: user.email,
            SpotifyFields.SPOTIFY_ID: user.spotify_id,
            SpotifyProfileFields.DISPLAY_NAME: profile.get('display_name'),
            SpotifyProfileFields.FOLLOWERS: profile.get('followers'),
            SpotifyProfileFields.HREF: profile.get('href'),
            SpotifyProfileFields.IMAGES: profile.get('images'),
            SpotifyProfileFields.TYPE: profile.get('type'),
            SpotifyProfileFields.URI: profile.get('uri')
        }
    })
