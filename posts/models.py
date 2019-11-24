import os
from django.core import validators
from django.db import models
from django.urls import reverse
from django.dispatch import receiver

from slugify import slugify

from news_project import settings


class PostApproveManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(status='APPROVE')


class Post(models.Model):
    MODERATION_CHOICES = [
        ('UNPUBLISHED', 'unpublished'),
        ('APPROVE', 'approve'),
        ('DECLINE', 'decline'),
    ]
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    slug = models.SlugField(max_length=200, unique=True, null=True, blank=True)
    title = models.CharField(max_length=200, unique=True)
    content = models.TextField()
    attachment = models.FileField(upload_to='files/', blank=True, null=True,
                            validators=[validators.FileExtensionValidator(
                                allowed_extensions=('jpg', 'jpeg', 'png'))],
                            error_messages={
                                'invalid_extension': 'Unsupported file extension'})
    updated_on = models.DateTimeField(auto_now=True)
    created_on = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=12, choices=MODERATION_CHOICES, default='UNPUBLISHED')

    objects = models.Manager() # Default manager
    approved = PostApproveManager()  # New manager for approved posts

    class Meta:
        ordering = ['-created_on']

    def __str__(self):
        return self.title

    def save(self,  *args, **kwargs):
        # set slug field for post
        self.slug = slugify(self.title)
        return super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('post_detail', kwargs={'slug': self.slug})


@receiver(models.signals.post_delete, sender=Post)
def auto_delete_file_on_delete(sender, instance, **kwargs):
    """
    Deletes file from filesystem
    when corresponding `Post` object is deleted.
    """
    if instance.attachment:
        if os.path.isfile(instance.attachment.path):
            os.remove(instance.attachment.path)

@receiver(models.signals.pre_save, sender=Post)
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
