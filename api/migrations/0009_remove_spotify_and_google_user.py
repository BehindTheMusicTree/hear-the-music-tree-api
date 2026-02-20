from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0008_copy_provider_data_to_user'),
    ]

    operations = [
        migrations.DeleteModel(name='SpotifyUser'),
        migrations.DeleteModel(name='GoogleUser'),
    ]
