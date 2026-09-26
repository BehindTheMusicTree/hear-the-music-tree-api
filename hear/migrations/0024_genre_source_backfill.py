from django.db import migrations


def backfill_source(apps, schema_editor):
    """Pre-0.28 genres all came from tree imports (which replaced the whole tree), and legacy exports carried no
    wikidata id, so every non-edited genre is treated as pipeline-owned."""
    Genre = apps.get_model("hear", "Genre")
    Genre.objects.filter(is_manually_edited=False).update(source="pipeline")
    Genre.objects.filter(is_manually_edited=True).update(source="admin")


class Migration(migrations.Migration):
    dependencies = [
        ("hear", "0023_genre_kit_multi_parent"),
    ]

    operations = [
        migrations.RunPython(backfill_source, migrations.RunPython.noop),
    ]
