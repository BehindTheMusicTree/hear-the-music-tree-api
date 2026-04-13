from api import settings
from api.exception import spotify as spotify_exception


class SpotifyCredentialManager:
    def __init__(self):
        self.client_id = settings.SPOTIFY_CLIENT_ID
        self.client_secret = settings.SPOTIFY_CLIENT_SECRET
        self.redirect_uri = settings.SPOTIFY_REDIRECT_URI
        self.scope = settings.SPOTIFY_SCOPES

    def get_client_credentials(self) -> dict:
        return {
            "client_id": self.client_id,
            "client_secret": self.client_secret,
            "redirect_uri": self.redirect_uri,
            "scope": self.scope,
        }

    def validate_credentials(self) -> None:
        missing = []
        if not self.client_id:
            missing.append("client_id")
        if not self.client_secret:
            missing.append("client_secret")
        if missing:
            raise spotify_exception.SpotifyAPIException(
                f"Spotify {' and '.join(missing)} {'is' if len(missing) == 1 else 'are'} not configured"
            )
