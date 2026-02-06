# api/migrations/0002_create_system_tmta_user
import os
from django.db import migrations, models
from django.core.management.base import CommandError


def create_tmta_user(apps, schema_editor):
    User = apps.get_model("api", "User")
    username = os.getenv("TMTA_USERNAME", None)

    if not username:
        raise CommandError(
            "⚠️ TMTA_USERNAME must be set in environment variables before running migrations."
        )

    user, created = User.objects.get_or_create(
        username=username,
        defaults={
            "is_system": True,
            "is_active": True,
            "is_staff": False,
            "is_superuser": False,
        }
    )

    if created:
        # Secure the account by making password unusable
        user.set_unusable_password()
        user.save()


class Migration(migrations.Migration):
    dependencies = [
        ("api", "0001_initial"),
    ]

    operations = [
        migrations.AddField(model_name='user', name='is_system', field=models.BooleanField(
            default=False, help_text='Designates a user as a system-owned account. Cannot log in.'), ),
        migrations.RunPython(create_tmta_user),
    ]
