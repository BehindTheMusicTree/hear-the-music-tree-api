import django.db.models.deletion
import the_music_tree_api_kit.field.foreign_key.AppForeignKey
from django.db import migrations


def copy_criteria_types_to_genre_kit(apps, schema_editor):
    OldCriteriaType = apps.get_model("api", "CriteriaType")
    NewCriteriaType = apps.get_model("the_music_tree_genre_kit", "CriteriaType")
    for row in OldCriteriaType.objects.all():
        NewCriteriaType.objects.get_or_create(pk=row.pk, defaults={"label": row.label})


def noop(apps, schema_editor):
    pass


class Migration(migrations.Migration):
    dependencies = [
        ("api", "0012_rename_audio_meta_analysis_disabled_to_afp_disabled"),
        ("the_music_tree_genre_kit", "0001_initial"),
    ]

    operations = [
        migrations.RunPython(copy_criteria_types_to_genre_kit, noop),
        migrations.AlterField(
            model_name="criteria",
            name="type",
            field=the_music_tree_api_kit.field.foreign_key.AppForeignKey.AppForeignKey(
                on_delete=django.db.models.deletion.CASCADE, to="the_music_tree_genre_kit.criteriatype"
            ),
        ),
        migrations.AlterField(
            model_name="criteriaplaylist",
            name="type",
            field=the_music_tree_api_kit.field.foreign_key.AppForeignKey.AppForeignKey(
                on_delete=django.db.models.deletion.CASCADE, to="the_music_tree_genre_kit.criteriatype"
            ),
        ),
        migrations.DeleteModel(
            name="CriteriaType",
        ),
    ]
