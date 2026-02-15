from django.db import migrations


def copy_spotify_data(apps, schema_editor):
    with schema_editor.connection.cursor() as cursor:
        cursor.execute("""
            UPDATE htmt_api_user u
            SET
                spotify_id = s.spotify_id,
                spotify_access_token = s.spotify_access_token,
                spotify_refresh_token = s.spotify_refresh_token,
                spotify_profile = s.spotify_profile,
                spotify_token_expires_at = s.spotify_token_expires_at,
                spotify_library_last_synced_at = s.spotify_library_last_synced_at,
                spotify_sync_in_progress = s.spotify_sync_in_progress
            FROM htmt_api_spotify_user s
            WHERE u.id = s.user_ptr_id
        """)


def copy_google_data(apps, schema_editor):
    with schema_editor.connection.cursor() as cursor:
        cursor.execute("""
            UPDATE htmt_api_user u
            SET
                google_id = g.google_id,
                google_access_token = g.google_access_token,
                google_refresh_token = g.google_refresh_token,
                google_profile = g.google_profile,
                google_token_expires_at = g.google_token_expires_at
            FROM htmt_api_google_user g
            WHERE u.id = g.user_ptr_id
        """)


def noop(apps, schema_editor):
    pass


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0007_unified_user_providers'),
    ]

    operations = [
        migrations.RunPython(copy_spotify_data, noop),
        migrations.RunPython(copy_google_data, noop),
    ]
