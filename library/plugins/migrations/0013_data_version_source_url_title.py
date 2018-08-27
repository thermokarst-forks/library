from django.db import migrations


class Migration(migrations.Migration):
    def migrate(apps, schema_editor):
        Plugin = apps.get_model('plugins', 'Plugin')

        for plugin in Plugin.objects.all():
            plugin.title = 'q2-%s' % plugin.name.lower().replace('_', '-')
            plugin.version = '2018.6'
            plugin.source_url = 'https://github.com/qiime2/%s' % plugin.title
            plugin.save()

    dependencies = [
        ('plugins', '0012_plugin_version'),
    ]

    operations = [
        migrations.RunPython(migrate, migrations.RunPython.noop),
    ]
