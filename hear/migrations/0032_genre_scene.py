import the_music_tree_api_kit.field
from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("hear", "0031_genre_description_genre_is_umbrella_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="genre",
            name="scene",
            field=the_music_tree_api_kit.field.AppCharField(
                blank=True,
                choices=[("commercial", "Commercial"), ("underground", "Underground")],
                db_column="scene",
                max_length=16,
                null=True,
            ),
        ),
    ]
