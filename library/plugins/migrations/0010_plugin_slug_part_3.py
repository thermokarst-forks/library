from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('plugins', '0009_plugin_slug_part_2'),
    ]

    operations = [
        migrations.AlterField(
            model_name='plugin',
            name='slug',
            field=models.SlugField(default='slug', max_length=500, unique=True),
        ),
    ]
