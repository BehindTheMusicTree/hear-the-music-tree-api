# app_name/migrations/0002_create_tmta_user.py
from django.db import migrations
import os


def create_tmta_user(apps, schema_editor):
    User = apps.get_model("api", "User")
    username = os.getenv("TMTA_USERNAME", None)
    password = os.getenv("TMTA_USER_PASSWORD", None)
    email = os.getenv("TMTA_EMAIL", None)

    if not username:
        raise CommandError(
            "⚠️ TMTA_USERNAME must be set in environment variables before running migrations."
        )
    if not password:
        raise CommandError(
            "⚠️ TMTA_USER_PASSWORD must be set in environment variables before running migrations."
        )
    if not email:
        raise CommandError(
            "⚠️ TMTA_EMAIL must be set in environment variables before running migrations."
        )

    tmta_user, created = User.objects.get_or_create(
        username=username,
        defaults={
            "email": email,
            "is_staff": True,
            "is_active": True,
            "is_superuser": False,
        },
    )


def remove_tmta_user(apps, schema_editor):
    User = apps.get_model("auth", "User")
    User.objects.filter(username="system").delete()


class Migration(migrations.Migration):
    dependencies = [
        ("app_name", "0001_initial"),
    ]

    operations = [
        migrations.RunPython(create_tmta_user, remove_tmta_user),
    ]
