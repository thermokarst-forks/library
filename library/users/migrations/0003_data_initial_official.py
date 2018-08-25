from django.db import migrations


class Migration(migrations.Migration):
    def migrate(apps, schema_editor):
        User = apps.get_model('users', 'User')
        user = User.objects.create(
            full_name='q2d2',
            username='q2d2',
            email='no-reply@qiime2.org',
        )

    def rollback(apps, schema_editor):
        User = apps.get_model('users', 'User')
        User.objects.all().delete()

    dependencies = [
        ('users', '0002_user_full_name'),
    ]

    operations = [
        migrations.RunPython(migrate, rollback),
    ]
