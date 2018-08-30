from django.db import migrations, models

from library.utils import slug


class Migration(migrations.Migration):
    def migrate(apps, schema_editor):
        Plugin = apps.get_model('plugins', 'Plugin')
        for plugin in Plugin.unsafe.all():
            plugin.slug = slug(plugin, 'title', 'slug')
            plugin.save()

    dependencies = [
        ('plugins', '0016_manager_switch'),
    ]

    operations = [
        migrations.AlterField(
            model_name='plugin',
            name='description',
            field=models.TextField(help_text='A free-form description of the plugin.'),
        ),
        migrations.AlterField(
            model_name='plugin',
            name='install_guide',
            field=models.TextField(help_text='This field should contain directions (or a link to directions) on how to install the plugin.'),
        ),
        migrations.AlterField(
            model_name='plugin',
            name='name',
            field=models.CharField(help_text="The plugin's name, as registered in QIIME 2. e.g. my_plugin", max_length=500, unique=True),
        ),
        migrations.AlterField(
            model_name='plugin',
            name='published',
            field=models.BooleanField(default=False, help_text='This field controls the plugin\'s visibility to other users on library.qiime2.org.  Only mark as "true" if you are prepared for the plugin to go "live"!'),
        ),
        migrations.AlterField(
            model_name='plugin',
            name='short_summary',
            field=models.CharField(help_text='This field is displayed in "overviews" such as the plugin listing page.', max_length=500),
        ),
        migrations.AlterField(
            model_name='plugin',
            name='title',
            field=models.CharField(help_text="The plugin's project title (e.g. q2-my-plugin).", max_length=500, unique=True),
        ),
        migrations.RunPython(migrate, migrations.RunPython.noop),
    ]
