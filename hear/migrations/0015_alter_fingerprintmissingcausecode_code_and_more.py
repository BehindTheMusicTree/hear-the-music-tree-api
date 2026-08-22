from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("hear", "0014_rename_uploaded_track_playlist_rel_to_track_playlist_rel"),
    ]

    operations = [
        migrations.AlterField(
            model_name="fingerprintmissingcausecode",
            name="code",
            field=models.IntegerField(
                choices=[
                    (0, "Afp Disabled"),
                    (1, "Service Not Found"),
                    (2, "Fpcalc Error With Status 2"),
                    (3, "Wrong File Extension"),
                    (4, "Wrong File Type"),
                    (5, "File Not Found In Pool"),
                    (6, "Unknown Bad Request"),
                    (7, "Internal Error"),
                    (8, "Timeout Error"),
                    (9, "Unknown Connexion Error"),
                    (10, "Unknown Unprocessable Entity Error"),
                ],
                primary_key=True,
                serialize=False,
                unique=True,
            ),
        ),
        migrations.AlterField(
            model_name="mbrecordingmissingcausecode",
            name="code",
            field=models.PositiveIntegerField(
                choices=[
                    (0, "Afp Disabled"),
                    (1, "Track File Fingerprinting Failed"),
                    (2, "Duration Below Or Equal 1 Sec"),
                    (3, "Lookup Found No Matching Recording"),
                    (4, "Lookup Failed Due To Invalid Fingerprint"),
                    (5, "Lookup Failed With Internal Error"),
                    (6, "Lookup Failed With Unknown Response Error Code"),
                    (7, "Lookup Failed With Unknown Response Status Code"),
                    (8, "Lookup Failed Dns Resolution Error"),
                    (9, "Musicbrainz Lookup Disabled"),
                ],
                primary_key=True,
                serialize=False,
                unique=True,
            ),
        ),
    ]
