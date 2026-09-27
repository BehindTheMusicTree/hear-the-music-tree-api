from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("hear", "0026_uploaded_track_archived"),
        ("the_music_tree_genre_kit", "0008_remove_track_archived"),
    ]

    operations = [
        migrations.SeparateDatabaseAndState(
            state_operations=[
                migrations.AddField(
                    model_name="uploadedtrack",
                    name="archived",
                    field=models.BooleanField(default=False),
                ),
            ],
        ),
    ]
