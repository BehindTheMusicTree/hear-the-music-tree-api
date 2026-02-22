from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0009_remove_spotify_and_google_user'),
    ]

    operations = [
        migrations.SeparateDatabaseAndState(
            state_operations=[
                migrations.AddField(
                    model_name='user',
                    name='spotify_id',
                    field=models.CharField(blank=True, max_length=255, null=True, unique=True),
                ),
                migrations.AddField(
                    model_name='user',
                    name='spotify_access_token',
                    field=models.TextField(blank=True, null=True),
                ),
                migrations.AddField(
                    model_name='user',
                    name='spotify_refresh_token',
                    field=models.TextField(blank=True, null=True),
                ),
                migrations.AddField(
                    model_name='user',
                    name='spotify_profile',
                    field=models.JSONField(blank=True, null=True),
                ),
                migrations.AddField(
                    model_name='user',
                    name='spotify_token_expires_at',
                    field=models.DateTimeField(blank=True, null=True),
                ),
                migrations.AddField(
                    model_name='user',
                    name='spotify_library_last_synced_at',
                    field=models.DateTimeField(blank=True, null=True),
                ),
                migrations.AddField(
                    model_name='user',
                    name='spotify_sync_in_progress',
                    field=models.BooleanField(blank=True, default=False, null=True),
                ),
                migrations.AddField(
                    model_name='user',
                    name='google_id',
                    field=models.CharField(blank=True, max_length=255, null=True, unique=True),
                ),
                migrations.AddField(
                    model_name='user',
                    name='google_access_token',
                    field=models.TextField(blank=True, null=True),
                ),
                migrations.AddField(
                    model_name='user',
                    name='google_refresh_token',
                    field=models.TextField(blank=True, null=True),
                ),
                migrations.AddField(
                    model_name='user',
                    name='google_profile',
                    field=models.JSONField(blank=True, null=True),
                ),
                migrations.AddField(
                    model_name='user',
                    name='google_token_expires_at',
                    field=models.DateTimeField(blank=True, null=True),
                ),
            ],
            database_operations=[],
        ),
    ]
