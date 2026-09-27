from django.db import migrations, models


class Migration(migrations.Migration):
    # Archiving moved from the kit Track into hear. The column is created and backfilled here, before the kit
    # drops its own; the model state gets the field in 0027, once the base-class field is gone (else it clashes).
    run_before = [
        ("the_music_tree_genre_kit", "0008_remove_track_archived"),
    ]

    dependencies = [
        ("hear", "0025_criteria_case_insensitive_unique_name"),
    ]

    operations = [
        migrations.AddField(
            model_name="genre",
            name="has_name_conflict",
            field=models.BooleanField(default=False),
        ),
        migrations.RunSQL(
            sql=[
                "ALTER TABLE htmt_api_uploaded_track ADD COLUMN archived boolean NOT NULL DEFAULT false",
                "ALTER TABLE htmt_api_uploaded_track ALTER COLUMN archived DROP DEFAULT",
                "UPDATE htmt_api_uploaded_track u SET archived = t.archived "
                "FROM the_music_tree_genre_kit_track t WHERE u.track_id = t.uuid",
            ],
            reverse_sql="ALTER TABLE htmt_api_uploaded_track DROP COLUMN archived",
        ),
    ]
