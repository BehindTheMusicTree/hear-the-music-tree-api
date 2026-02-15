from django.db import models

from api.model.user.User import User
from api.model.user.UserManager import UserManager


class GoogleUser(User):
    google_id = models.CharField(max_length=255, unique=True)
    google_access_token = models.TextField(null=True, blank=True)
    google_refresh_token = models.TextField(null=True, blank=True)
    google_profile = models.JSONField(null=True, blank=True)
    google_token_expires_at = models.DateTimeField(null=True, blank=True)

    objects: UserManager = UserManager['GoogleUser']()

    def __str__(self):
        return f"{self.username} (Google)"

    class Meta:
        verbose_name = 'Google User'
        verbose_name_plural = 'Google Users'
