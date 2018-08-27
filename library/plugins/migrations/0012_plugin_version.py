# Generated by Django 2.1 on 2018-08-27 17:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('plugins', '0011_plugin_title'),
    ]

    operations = [
        migrations.AddField(
            model_name='plugin',
            name='version',
            field=models.TextField(blank=True),
        ),
        migrations.AlterField(
            model_name='plugin',
            name='name',
            field=models.CharField(help_text="The plugin's name, as registered in QIIME 2.", max_length=500, unique=True),
        ),
    ]
