from django.db import migrations, models

# Three-part migration:
# https://docs.djangoproject.com/en/2.1/howto/writing-migrations/#migrations-that-add-unique-fields


class Migration(migrations.Migration):

    dependencies = [
        ('plugins', '0009_plugin_slug_part_2'),
    ]

    operations = [
        migrations.AlterField(
            model_name='plugin',
            name='slug',
            field=models.SlugField(max_length=500, unique=True),
        ),
    ]
