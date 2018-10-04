from django.db import migrations


class Migration(migrations.Migration):
    def manage(apps, schema_editor):
        from django.contrib.auth.models import Group, Permission
        from django.contrib.auth.management import create_permissions

        # Necessary to get the auto-gen model perms in place
        for app_config in apps.get_app_configs():
            app_config.models_module = True
            create_permissions(app_config, apps=apps, verbosity=0)
            app_config.models_module = None

        # This group may or may not exist, depending on our context (tests, prod, etc.)
        g, _ = Group.objects.get_or_create(name='forum_trust_level_1')
        p = Permission.objects.get(codename='add_plugin')
        g.permissions.add(p)

    dependencies = [
        ('users', '0001_initial'),
        ('plugins', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(manage, migrations.RunPython.noop),
    ]
