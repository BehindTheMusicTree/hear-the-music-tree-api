import django.db.models.deletion
import the_music_tree_api_kit.field.foreign_key.PrivateForeignKey
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("api", "0013_move_criteria_type_to_genre_kit"),
    ]

    operations = [
        migrations.RenameModel(
            old_name="UploadedTrackPlaylistRel",
            new_name="TrackPlaylistRel",
        ),
        migrations.RenameField(
            model_name="trackplaylistrel",
            old_name="uploaded_track",
            new_name="track",
        ),
        migrations.AlterModelOptions(
            name="trackplaylistrel",
            options={
                "verbose_name": "Track Playlist Relation",
                "verbose_name_plural": "Track Playlist Relations",
            },
        ),
        migrations.AlterField(
            model_name="trackplaylistrel",
            name="playlist",
            field=the_music_tree_api_kit.field.foreign_key.PrivateForeignKey.PrivateForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="track_playlist_rels",
                to="api.playlist",
            ),
        ),
        migrations.AlterField(
            model_name="trackplaylistrel",
            name="track",
            field=the_music_tree_api_kit.field.foreign_key.PrivateForeignKey.PrivateForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="track_playlist_rels",
                to="api.uploadedtrack",
            ),
        ),
        migrations.RemoveIndex(
            model_name="trackplaylistrel",
            name="htmt_api_up_user_id_6ab4bf_idx",
        ),
        migrations.AddIndex(
            model_name="trackplaylistrel",
            index=models.Index(fields=["user", "track"], name="htmt_api_up_user_id_e183ff_idx"),
        ),
    ]
