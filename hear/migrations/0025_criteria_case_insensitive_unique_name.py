import django.db.models.functions.text
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("hear", "0024_genre_source_backfill"),
    ]

    operations = [
        migrations.RemoveConstraint(
            model_name="criteria",
            name="unique_name_per_user",
        ),
        migrations.AddConstraint(
            model_name="criteria",
            constraint=models.UniqueConstraint(
                django.db.models.functions.text.Lower("_name"), models.F("user"), name="unique_name_per_user"
            ),
        ),
    ]
