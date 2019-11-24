"""
Create default groups
"""

from django.core.management.base import BaseCommand

from django.contrib.auth.models import Group

class Command(BaseCommand):
    help = 'Creates default groups for users'

    def handle(self, *args, **options):
        Group.objects.create(name='admins')
        Group.objects.create(name='editors')
        Group.objects.create(name='users')
