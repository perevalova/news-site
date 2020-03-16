import os

from django.contrib.auth import get_user_model
from django.db.models.signals import post_delete, pre_save, post_save, m2m_changed
from django.dispatch import receiver

from news_project import settings
from posts.models import Post, PersonalBlog


@receiver(post_delete, sender=Post)
def auto_delete_file_on_delete(sender, instance, **kwargs):
    """
    Deletes file from filesystem
    when corresponding `Post` object is deleted.
    """
    if instance.attachment:
        if os.path.isfile(instance.attachment.path):
            os.remove(instance.attachment.path)


@receiver(pre_save, sender=Post)
def auto_delete_file_on_change(sender, instance, **kwargs):
    """
    Deletes old file from filesystem
    when corresponding `Post` object is updated
    with new file.
    """
    if not instance.pk:
        return False

    try:
        old_file = Post.objects.get(pk=instance.pk).attachment
    except Post.DoesNotExist:
        return False

    new_attachment = instance.attachment
    if not old_file == new_attachment:
        if os.path.isfile(old_file.path):
            os.remove(old_file.path)


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_personal_blog(sender, instance, created, **kwargs):
    """
    Create blog for user
    """
    if created:
        PersonalBlog.objects.create(author=instance)


@receiver(m2m_changed, sender=PersonalBlog.subscriptions.through)
def followers_and_read_post(sender, instance, action, reverse, *args, **kwargs):
    """
    Add or remove followers when changing subscriptions.
    Also remove read posts when remove subscription.
    """
    if action == 'pre_add':
        author = instance.author_id # id of author that added subscription
        User = get_user_model()
        user = User.objects.get(id=author)
        sub = kwargs['pk_set'] # id of added subscription
        for pk in sub:
            pb = PersonalBlog.objects.get(author_id=pk)
            pb.followers.add(user)
    if action == 'pre_remove':
        author = instance.author_id # id of author that removed subscription
        User = get_user_model()
        user = User.objects.get(id=author)
        sub = kwargs['pk_set'] # id of removed subscription
        for pk in sub:
            pb = PersonalBlog.objects.get(author_id=pk)
            pb.followers.remove(user)
            # removing read posts of removed subscription
            posts = Post.objects.filter(author_id=pk)
            instance.read_posts.remove(*posts)
