from django.db import migrations, models

# Three-part migration:
# https://docs.djangoproject.com/en/2.1/howto/writing-migrations/#migrations-that-add-unique-fields


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
