from django.contrib.auth.models import Group
from django.db.models.signals import post_save
from django.dispatch import receiver

from news_project import settings


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_user_profile(sender, instance, created, **kwargs):
    """
    Add new user to 'users' group
    """
    if created:
        instance.groups.add(Group.objects.get(name='users'))