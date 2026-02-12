from django.db import migrations


def seed_criteria_types(apps, schema_editor):
    CriteriaType = apps.get_model("api", "CriteriaType")
    CriteriaType.objects.get_or_create(pk=0, defaults={"label": "genre"})
    CriteriaType.objects.get_or_create(pk=1, defaults={"label": "tag"})


def noop(apps, schema_editor):
    pass


class Migration(migrations.Migration):
    dependencies = [
        ("api", "0002_create_system_tmta_user"),
    ]

    operations = [
        migrations.RunPython(seed_criteria_types, noop),
    ]
