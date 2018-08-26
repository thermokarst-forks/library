from django.db import migrations

from library.utils import slug

# Three-part migration:
# https://docs.djangoproject.com/en/2.1/howto/writing-migrations/#migrations-that-add-unique-fields


class Migration(migrations.Migration):
    def migrate(apps, schema_editor):
        Plugin = apps.get_model('plugins', 'Plugin')
        for plugin in Plugin.objects.all():
            # Signals are disabled in migrations, need to manually add.
            plugin.slug = slug(plugin, 'name', 'slug')
            plugin.save()

    dependencies = [
        ('plugins', '0008_plugin_slug_part_1'),
    ]

    operations = [
        migrations.RunPython(migrate, migrations.RunPython.noop),
    ]
