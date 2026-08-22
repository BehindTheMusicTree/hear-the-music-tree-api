from django.db import migrations


def seed_fingerprint_missing_cause_codes(apps, schema_editor):
    FingerprintMissingCauseCode = apps.get_model("hear", "FingerprintMissingCauseCode")

    data = [
        (0, "The audio meta analysis is disabled."),
        (1, "The Audio Fingerprinter service was not found."),
        (
            2,
            "The use of the fpcalc software in the Audio Fingerprinter service failed with status 2. The file may be corrupted.",
        ),
        (3, "The Audio Fingerprinter service does not support the files's extension."),
        (4, "The Audio Fingerprinter service does not handle the files's type."),
        (
            5,
            "The Audio Fingerprinter could not find the specified file in the pool directory.",
        ),
        (
            6,
            "The Audio Fingerprinter returned a 400 Bad Request response that could not be analysed.",
        ),
        (7, "The Audio Fingerprinter returned a 500 Internal Error."),
        (8, "The Audio Fingerprinter returned a 504 timeout error."),
        (
            9,
            "The connexion to the Audio Fingerprinter could not be established for an unknown reason.",
        ),
        (
            10,
            "The Audio Fingerprinter service returned an unknown 422 Unprocessable Entity error.",
        ),
    ]

    for code, label in data:
        FingerprintMissingCauseCode.objects.get_or_create(
            code=code,
            defaults={"label": label},
        )


def seed_mb_recording_missing_cause_codes(apps, schema_editor):
    MbRecordingMissingCauseCode = apps.get_model("hear", "MbRecordingMissingCauseCode")

    data = [
        (0, "The audio meta analysis is disabled."),
        (1, "The track's file is missing."),
        (
            2,
            "The track's duration is below or equals 1 second. MusicBrainz won't lookup.",
        ),
        (3, "The Musicbrainz lookup did not find a matching recording."),
        (
            4,
            "The MusicBrainz lookup failed with status code 3 (invalid fingerprint).",
        ),
        (
            5,
            "The MusicBrainz lookup failed with status code 5 (internal error).",
        ),
        (
            6,
            "The MusicBrainz lookup failed with an unknown error code.",
        ),
        (
            7,
            "The MusicBrainz lookup failed with an unknown status code.",
        ),
        (
            8,
            "The MusicBrainz lookup failed resolving MusicBrainz DNS.",
        ),
    ]

    for code, label in data:
        MbRecordingMissingCauseCode.objects.get_or_create(
            code=code,
            defaults={"label": label},
        )


def noop(apps, schema_editor):
    pass


class Migration(migrations.Migration):
    dependencies = [
        ("hear", "0003_seed_criteria_types"),
    ]

    operations = [
        migrations.RunPython(
            seed_fingerprint_missing_cause_codes,
            noop,
        ),
        migrations.RunPython(
            seed_mb_recording_missing_cause_codes,
            noop,
        ),
    ]
