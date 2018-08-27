from django.db import migrations


class Migration(migrations.Migration):
    def migrate(apps, schema_editor):
        Plugin = apps.get_model('plugins', 'Plugin')

        plugins = {
            # `types` has no deps, not listed here.
            'feature-table': ['types'],
            'alignment': ['types'],
            'composition': ['types'],
            'dada2': ['types'],
            'deblur': ['types'],
            'demux': ['types'],
            'diversity': ['types', 'feature-table', 'emperor', 'metadata'],
            'emperor': ['types'],
            'feature-classifier': ['types'],
            'metadata': ['types'],
            'phylogeny': ['types', 'alignment'],
            'quality-filter': ['types'],
            'taxa': ['types'],
            'gneiss': ['types'],
            'sample-classifier': ['types', 'feature-table', 'longitudinal'],
            'longitudinal': ['types', 'sample-classifier'],
            'vsearch': ['types', 'feature-table'],
            'quality-control': ['types', 'taxa'],
            'cutadapt': ['types'],
        }
        for name, deps in plugins.items():
            # this isn't super efficient this way, but that shouldn't be a problem here...
            plugin = Plugin.objects.get(name=name)
            for dep in deps:
                d = Plugin.objects.get(name=dep)
                plugin.dependencies.add(d)
            plugin.save()

    dependencies = [
        ('plugins', '0014_plugin_dependencies'),
    ]

    operations = [
        migrations.RunPython(migrate, migrations.RunPython.noop),
    ]
