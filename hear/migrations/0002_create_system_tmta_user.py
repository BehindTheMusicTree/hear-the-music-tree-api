# hear/migrations/0002_create_system_tmta_user
import os

from django.contrib.auth.hashers import make_password
from django.core.management.base import CommandError
from django.db import migrations, models


def create_tmta_user(apps, schema_editor):
    User = apps.get_model("hear", "User")
    username = os.getenv("TMTA_USERNAME", None)

    if not username:
        raise CommandError("⚠️ TMTA_USERNAME must be set in environment variables before running migrations.")

    user, _created = User.objects.get_or_create(
        username=username,
        defaults={
            "is_system": True,
            "is_active": True,
            "is_staff": False,
            "is_superuser": False,
        },
    )

    # enforce unusable password even if user already existed
    if user.password and not user.password.startswith("!"):
        user.password = make_password(None)
        user.save(update_fields=["password"])


class Migration(migrations.Migration):
    dependencies = [
        ("hear", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="user",
            name="is_system",
            field=models.BooleanField(
                default=False, help_text="Designates a user as a system-owned account. Cannot log in."
            ),
        ),
        migrations.RunPython(create_tmta_user),
    ]
