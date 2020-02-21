import os

from django.db.models.signals import post_delete, pre_save
from django.dispatch import receiver

from posts.models import Post


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
