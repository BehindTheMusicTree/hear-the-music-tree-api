from django.db import migrations, models


def forwards(apps, schema_editor):
    apps.get_model("hear", "Criteria").objects.filter(allows_multiple_primary_parents=True).update(tree_name="regional")


def backwards(apps, schema_editor):
    apps.get_model("hear", "Criteria").objects.filter(tree_name="regional").update(allows_multiple_primary_parents=True)


class Migration(migrations.Migration):
    dependencies = [
        ("hear", "0028_genre_is_unaccepted_root"),
    ]

    operations = [
        migrations.AddField(
            model_name="criteria",
            name="tree_name",
            field=models.CharField(
                choices=[("canonical", "Canonical"), ("regional", "Regional")], default="canonical", max_length=16
            ),
        ),
        migrations.RunPython(forwards, backwards),
        migrations.RemoveField(
            model_name="criteria",
            name="allows_multiple_primary_parents",
        ),
    ]
