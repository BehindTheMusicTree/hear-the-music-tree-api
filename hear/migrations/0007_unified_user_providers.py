from django.db import migrations


def add_columns(apps, schema_editor):
    with schema_editor.connection.cursor() as cursor:
        cursor.execute("ALTER TABLE htmt_api_user ADD COLUMN IF NOT EXISTS spotify_id VARCHAR(255) UNIQUE NULL")
        cursor.execute("ALTER TABLE htmt_api_user ADD COLUMN IF NOT EXISTS spotify_access_token TEXT NULL")
        cursor.execute("ALTER TABLE htmt_api_user ADD COLUMN IF NOT EXISTS spotify_refresh_token TEXT NULL")
        cursor.execute("ALTER TABLE htmt_api_user ADD COLUMN IF NOT EXISTS spotify_profile JSONB NULL")
        cursor.execute(
            "ALTER TABLE htmt_api_user ADD COLUMN IF NOT EXISTS spotify_token_expires_at TIMESTAMP WITH TIME ZONE NULL"
        )
        cursor.execute(
            "ALTER TABLE htmt_api_user ADD COLUMN IF NOT EXISTS spotify_library_last_synced_at TIMESTAMP WITH TIME ZONE NULL"
        )
        cursor.execute(
            "ALTER TABLE htmt_api_user ADD COLUMN IF NOT EXISTS spotify_sync_in_progress BOOLEAN NULL DEFAULT FALSE"
        )
        cursor.execute("ALTER TABLE htmt_api_user ADD COLUMN IF NOT EXISTS google_id VARCHAR(255) UNIQUE NULL")
        cursor.execute("ALTER TABLE htmt_api_user ADD COLUMN IF NOT EXISTS google_access_token TEXT NULL")
        cursor.execute("ALTER TABLE htmt_api_user ADD COLUMN IF NOT EXISTS google_refresh_token TEXT NULL")
        cursor.execute("ALTER TABLE htmt_api_user ADD COLUMN IF NOT EXISTS google_profile JSONB NULL")
        cursor.execute(
            "ALTER TABLE htmt_api_user ADD COLUMN IF NOT EXISTS google_token_expires_at TIMESTAMP WITH TIME ZONE NULL"
        )


def drop_columns(apps, schema_editor):
    with schema_editor.connection.cursor() as cursor:
        for col in [
            "spotify_id",
            "spotify_access_token",
            "spotify_refresh_token",
            "spotify_profile",
            "spotify_token_expires_at",
            "spotify_library_last_synced_at",
            "spotify_sync_in_progress",
            "google_id",
            "google_access_token",
            "google_refresh_token",
            "google_profile",
            "google_token_expires_at",
        ]:
            cursor.execute(f"ALTER TABLE htmt_api_user DROP COLUMN IF EXISTS {col}")


class Migration(migrations.Migration):
    dependencies = [
        ("hear", "0006_google_user"),
    ]

    operations = [
        migrations.SeparateDatabaseAndState(
            state_operations=[],
            database_operations=[
                migrations.RunPython(add_columns, drop_columns),
            ],
        ),
    ]
