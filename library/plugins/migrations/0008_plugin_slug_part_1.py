from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('plugins', '0007_plugin_default_manager'),
    ]

    operations = [
        migrations.AddField(
            model_name='plugin',
            name='slug',
            field=models.SlugField(default='slug', max_length=500, blank=True),
        ),
    ]
