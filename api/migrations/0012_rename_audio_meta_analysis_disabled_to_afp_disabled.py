from django.db import migrations

NEW_LABEL = "AFP (fingerprinting) is disabled."


def update_labels(apps, schema_editor):
    FingerprintMissingCauseCode = apps.get_model("api", "FingerprintMissingCauseCode")
    MbRecordingMissingCauseCode = apps.get_model("api", "MbRecordingMissingCauseCode")

    FingerprintMissingCauseCode.objects.filter(code=0).update(label=NEW_LABEL)
    MbRecordingMissingCauseCode.objects.filter(code=0).update(label=NEW_LABEL)


def reverse_labels(apps, schema_editor):
    old_label = "The audio meta analysis is disabled."
    FingerprintMissingCauseCode = apps.get_model("api", "FingerprintMissingCauseCode")
    MbRecordingMissingCauseCode = apps.get_model("api", "MbRecordingMissingCauseCode")

    FingerprintMissingCauseCode.objects.filter(code=0).update(label=old_label)
    MbRecordingMissingCauseCode.objects.filter(code=0).update(label=old_label)


class Migration(migrations.Migration):
    dependencies = [
        ("api", "0011_seed_musicbrainz_lookup_disabled_code"),
    ]

    operations = [
        migrations.RunPython(update_labels, reverse_labels),
    ]
