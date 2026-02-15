class GoogleAuthenticationException(Exception):
    """Raised when authentication with Google OAuth fails."""

    def __init__(self, message: str, *, detail_code: str | None = None):
        super().__init__(message)
        self.detail_code = detail_code or "google_authentication_error"
