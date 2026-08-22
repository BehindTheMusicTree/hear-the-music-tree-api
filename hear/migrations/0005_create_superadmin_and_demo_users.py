# hear/migrations/0005_create_superadmin_and_demo_users
import os

from django.contrib.auth.hashers import make_password
from django.core.management.base import CommandError
from django.db import migrations


def create_superadmin_user(apps, schema_editor):
    User = apps.get_model("hear", "User")
    username = os.getenv("SUPERADMIN_USERNAME")
    password = os.getenv("SUPERADMIN_PASSWORD")
    if not username:
        raise CommandError("SUPERADMIN_USERNAME must be set in environment variables before running migrations.")
    if not password:
        raise CommandError("SUPERADMIN_PASSWORD must be set in environment variables before running migrations.")
    email = os.getenv("SUPERADMIN_EMAIL", "").strip() or f"{username}@example.com"
    user, _created = User.objects.get_or_create(
        username=username,
        defaults={
            "email": email,
            "is_active": True,
            "is_staff": True,
            "is_superuser": True,
            "is_system": False,
        },
    )
    user.password = make_password(password)
    user.email = email
    user.is_staff = True
    user.is_superuser = True
    user.is_active = True
    user.save(update_fields=["password", "email", "is_staff", "is_superuser", "is_active"])


def create_demo_user(apps, schema_editor):
    User = apps.get_model("hear", "User")
    username = os.getenv("DEMO_USERNAME")
    password = os.getenv("DEMO_PASSWORD")
    if not username:
        raise CommandError("DEMO_USERNAME must be set in environment variables before running migrations.")
    if not password:
        raise CommandError("DEMO_PASSWORD must be set in environment variables before running migrations.")
    email = os.getenv("DEMO_EMAIL", "").strip() or f"{username}@example.com"
    user, _created = User.objects.get_or_create(
        username=username,
        defaults={
            "email": email,
            "is_active": True,
            "is_staff": False,
            "is_superuser": False,
            "is_system": False,
        },
    )
    user.password = make_password(password)
    user.email = email
    user.is_active = True
    user.save(update_fields=["password", "email", "is_active"])


def noop(apps, schema_editor):
    pass


class Migration(migrations.Migration):
    dependencies = [
        ("hear", "0004_seed_missing_cause_codes"),
    ]

    operations = [
        migrations.RunPython(create_superadmin_user, noop),
        migrations.RunPython(create_demo_user, noop),
    ]
