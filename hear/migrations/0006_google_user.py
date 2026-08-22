import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("hear", "0005_create_superadmin_and_demo_users"),
    ]

    operations = [
        migrations.CreateModel(
            name="GoogleUser",
            fields=[
                (
                    "user_ptr",
                    models.OneToOneField(
                        auto_created=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        parent_link=True,
                        primary_key=True,
                        serialize=False,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                ("google_id", models.CharField(max_length=255, unique=True)),
                ("google_access_token", models.TextField(blank=True, null=True)),
                ("google_refresh_token", models.TextField(blank=True, null=True)),
                ("google_profile", models.JSONField(blank=True, null=True)),
                ("google_token_expires_at", models.DateTimeField(blank=True, null=True)),
            ],
            options={
                "verbose_name": "Google User",
                "verbose_name_plural": "Google Users",
                "db_table": "htmt_api_google_user",
            },
            bases=("hear.user",),
        ),
    ]
