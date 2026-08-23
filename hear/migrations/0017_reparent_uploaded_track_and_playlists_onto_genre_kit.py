import django.db.models.deletion
import the_music_tree_api_kit.field
import the_music_tree_api_kit.field.foreign_key.AppForeignKey
import the_music_tree_api_kit.field.foreign_key.PrivateForeignKey
import the_music_tree_api_kit.field.foreign_key.PrivateOneToOneField
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("hear", "0016_remove_stale_playlist_user_uuid_index"),
        ("the_music_tree_genre_kit", "0005_trackplaylistrel_track_playlists_and_more"),
    ]

    operations = [
        migrations.DeleteModel(name="TrackPlaylistRel"),
        migrations.DeleteModel(name="ManualPlaylist"),
        migrations.DeleteModel(name="CriteriaPlaylist"),
        migrations.DeleteModel(name="UploadedTrack"),
        migrations.DeleteModel(name="Playlist"),
        migrations.CreateModel(
            name="UploadedTrack",
            fields=[
                (
                    "track",
                    the_music_tree_api_kit.field.foreign_key.PrivateOneToOneField.PrivateOneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        parent_link=True,
                        primary_key=True,
                        related_name="uploadedtrack",
                        serialize=False,
                        to="the_music_tree_genre_kit.track",
                    ),
                ),
                ("track_file_fingerprint_must_be_unique", models.BooleanField(default=False)),
            ],
            options={
                "verbose_name": "Uploaded Track",
                "verbose_name_plural": "Uploaded Tracks",
                "db_table": "htmt_api_uploaded_track",
            },
            bases=("the_music_tree_genre_kit.track",),
        ),
        migrations.CreateModel(
            name="CriteriaPlaylist",
            fields=[
                (
                    "playlist",
                    the_music_tree_api_kit.field.foreign_key.PrivateOneToOneField.PrivateOneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        parent_link=True,
                        primary_key=True,
                        related_name="criteria_playlist",
                        serialize=False,
                        to="the_music_tree_genre_kit.playlist",
                    ),
                ),
                (
                    "criteria",
                    the_music_tree_api_kit.field.foreign_key.PrivateOneToOneField.PrivateOneToOneField(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="criteria_playlist",
                        to="hear.criteria",
                    ),
                ),
                (
                    "parent",
                    the_music_tree_api_kit.field.foreign_key.PrivateForeignKey.PrivateForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="children",
                        to="hear.criteriaplaylist",
                    ),
                ),
                (
                    "root",
                    the_music_tree_api_kit.field.foreign_key.PrivateForeignKey.PrivateForeignKey(
                        on_delete=django.db.models.deletion.DO_NOTHING,
                        related_name="root_descendants",
                        to="hear.criteriaplaylist",
                    ),
                ),
                (
                    "type",
                    the_music_tree_api_kit.field.foreign_key.AppForeignKey.AppForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="the_music_tree_genre_kit.criteriatype"
                    ),
                ),
            ],
            options={
                "verbose_name": "Criteria Playlist",
                "verbose_name_plural": "Criteria Playlists",
                "db_table": "htmt_api_criteria_playlist",
            },
            bases=("the_music_tree_genre_kit.playlist",),
        ),
        migrations.CreateModel(
            name="ManualPlaylist",
            fields=[
                (
                    "playlist",
                    the_music_tree_api_kit.field.foreign_key.PrivateOneToOneField.PrivateOneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        parent_link=True,
                        primary_key=True,
                        related_name="manual_playlist",
                        serialize=False,
                        to="the_music_tree_genre_kit.playlist",
                    ),
                ),
                ("_name", the_music_tree_api_kit.field.AppCharField(db_column="name", max_length=256)),
            ],
            options={
                "verbose_name": "Manual Playlist",
                "verbose_name_plural": "Manual Playlists",
                "db_table": "htmt_api_manual_playlist",
            },
            bases=("the_music_tree_genre_kit.playlist",),
        ),
        migrations.AddIndex(
            model_name="criteriaplaylist",
            index=models.Index(fields=["criteria"], name="crit_playlist_criteria_idx"),
        ),
        migrations.AddIndex(
            model_name="manualplaylist",
            index=models.Index(fields=["_name"], name="manual_playlist_name_idx"),
        ),
        migrations.AddConstraint(
            model_name="manualplaylist",
            constraint=models.CheckConstraint(
                condition=models.Q(("_name", ""), _negated=True), name="manual_playlist_non_empty_name"
            ),
        ),
    ]
