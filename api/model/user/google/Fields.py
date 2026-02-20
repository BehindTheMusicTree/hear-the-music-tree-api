from api.model.user.Fields import Fields as UserFields


class Fields(UserFields):
    GOOGLE_ID: str = "google_id"
    GOOGLE_ACCESS_TOKEN: str = "google_access_token"
    GOOGLE_REFRESH_TOKEN: str = "google_refresh_token"
    GOOGLE_PROFILE: str = "google_profile"
    GOOGLE_TOKEN_EXPIRES_AT: str = "google_token_expires_at"
