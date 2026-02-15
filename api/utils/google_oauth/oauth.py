import logging
from typing import TypedDict

import requests
from django.conf import settings

from api.exception.google import GoogleAuthenticationException

logger = logging.getLogger(settings.APP_NAME)

GOOGLE_TOKEN_URL = "https://oauth2.googleapis.com/token"
GOOGLE_USERINFO_URL = "https://www.googleapis.com/oauth2/v2/userinfo"


class GoogleTokenInfo(TypedDict):
    access_token: str
    refresh_token: str | None
    expires_in: int
    id_token: str | None


class GoogleOAuthService:
    def __init__(self):
        self.client_id = settings.GOOGLE_CLIENT_ID
        self.client_secret = settings.GOOGLE_CLIENT_SECRET
        self.redirect_uri = settings.GOOGLE_REDIRECT_URI

    def exchange_code_for_tokens(self, code: str) -> GoogleTokenInfo:
        try:
            response = requests.post(
                GOOGLE_TOKEN_URL,
                data={
                    "code": code,
                    "client_id": self.client_id,
                    "client_secret": self.client_secret,
                    "redirect_uri": self.redirect_uri,
                    "grant_type": "authorization_code",
                },
                headers={"Content-Type": "application/x-www-form-urlencoded"},
                timeout=30,
            )
            response.raise_for_status()
            data = response.json()
            access_token = data.get("access_token")
            if not access_token:
                raise GoogleAuthenticationException("No access_token in Google token response")
            return {
                "access_token": access_token,
                "refresh_token": data.get("refresh_token"),
                "expires_in": int(data.get("expires_in", 3600)),
                "id_token": data.get("id_token"),
            }
        except requests.RequestException as e:
            if hasattr(e, "response") and e.response is not None:
                try:
                    body = e.response.json()
                    error_code = body.get("error")
                    msg = body.get("error_description", body.get("error", str(e)))
                    if error_code == "invalid_grant":
                        msg = (
                            "Authorization code already used, expired, or invalid. "
                            "Please try signing in again from the login page."
                        )
                        detail_code = "google_oauth_code_invalid_or_expired"
                    elif error_code == "redirect_uri_mismatch":
                        detail_code = "google_oauth_redirect_uri_mismatch"
                        msg = "Redirect URI does not match. Backend GOOGLE_REDIRECT_URI must match the frontend callback URL exactly."
                    elif error_code == "invalid_client":
                        detail_code = "google_oauth_invalid_client"
                        msg = "Invalid Google OAuth client configuration (client_id or client_secret)."
                    else:
                        detail_code = None
                    logger.error(
                        "Google token exchange failed: %s (error=%s)",
                        msg,
                        error_code,
                        extra={"response_body": body},
                    )
                except Exception:
                    msg = str(e)
                    detail_code = None
                    logger.error("Google token exchange failed: %s", e)
            else:
                msg = str(e)
                detail_code = None
                logger.error("Google token exchange failed: %s", e)
            raise GoogleAuthenticationException(
                f"Failed to exchange code for tokens: {msg}", detail_code=detail_code
            ) from e

    def get_user_info(self, access_token: str) -> dict:
        try:
            response = requests.get(
                GOOGLE_USERINFO_URL,
                headers={"Authorization": f"Bearer {access_token}"},
                timeout=30,
            )
            response.raise_for_status()
            data = response.json()
            if not data.get("id"):
                raise GoogleAuthenticationException("No user id in Google userinfo response")
            return data
        except requests.RequestException as e:
            logger.error("Google userinfo failed: %s", e)
            if hasattr(e, "response") and e.response is not None:
                try:
                    body = e.response.json()
                    msg = body.get("error_description", body.get("error", str(e)))
                except Exception:
                    msg = str(e)
            else:
                msg = str(e)
            raise GoogleAuthenticationException(f"Failed to get user info: {msg}") from e
