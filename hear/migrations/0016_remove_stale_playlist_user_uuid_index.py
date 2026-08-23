from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("hear", "0015_alter_fingerprintmissingcausecode_code_and_more"),
    ]

    run_before = [
        ("the_music_tree_genre_kit", "0004_playlist"),
    ]

    operations = [
        migrations.RemoveIndex(
            model_name="playlist",
            name="playlist_user_uuid_idx",
        ),
    ]
