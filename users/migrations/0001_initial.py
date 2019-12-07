# Generated by Django 2.2.7 on 2019-12-07 20:54

from django.conf import settings
from django.db import migrations


def apply_migration(apps, schema_editor):
    Group = apps.get_model('auth', 'Group')
    Group.objects.bulk_create(
        [Group(name='admins'), Group(name='editors'), Group(name='users')]
    )


def revert_migration(apps, schema_editor):
    Group = apps.get_model('auth', 'Group')
    Group.objects.filter(name__in=['admins', 'editors', 'users']).delete()


class Migration(migrations.Migration):
    dependencies = [
        ('auth', '0011_update_proxy_permissions'),
    ]

    operations = [
        migrations.RunPython(apply_migration, revert_migration),
    ]

    run_before = [
        ('admin', '0001_initial'),
    ]
