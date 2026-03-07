from django.db import migrations


def seed_musicbrainz_lookup_disabled_code(apps, schema_editor):
    MbRecordingMissingCauseCode = apps.get_model("api", "MbRecordingMissingCauseCode")
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
