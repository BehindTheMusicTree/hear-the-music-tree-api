from django.db import migrations


def _table_exists(cursor, table_name: str) -> bool:
    cursor.execute(
        """
        SELECT 1 FROM information_schema.tables
        WHERE table_schema = 'public' AND table_name = %s
        """,
        [table_name],
    )
    return cursor.fetchone() is not None


def seed_musicbrainz_lookup_disabled_code(apps, schema_editor):
    MbRecordingMissingCauseCode = apps.get_model("api", "MbRecordingMissingCauseCode")
    table = MbRecordingMissingCauseCode._meta.db_table
    with schema_editor.connection.cursor() as cursor:
        if not _table_exists(cursor, table):
            return
    MbRecordingMissingCauseCode.objects.get_or_create(
        code=9,
        defaults={"label": "MusicBrainz lookup is disabled."},
    )


def noop(apps, schema_editor):
    pass


class Migration(migrations.Migration):

    dependencies = [
        ("api", "0010_add_provider_fields_to_user_state"),
    ]

    operations = [
        migrations.RunPython(seed_musicbrainz_lookup_disabled_code, noop),
    ]
