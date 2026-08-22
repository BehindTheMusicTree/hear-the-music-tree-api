from rest_framework_simplejwt.tokens import AccessToken, RefreshToken


def create_jwt_token(user) -> dict:
    """
    Create JWT tokens for the given user.

    Returns:
        access: JWT access token string
        refresh: JWT refresh token string
        expires_at_ms: Unix timestamp in milliseconds when the access token expires
    """
    refresh = RefreshToken.for_user(user)
    access = AccessToken.for_user(user)
    expires_at_ms = int(access.payload["exp"]) * 1000
    return {
        "access": str(access),
        "refresh": str(refresh),
        "expires_at_ms": expires_at_ms,
    }
