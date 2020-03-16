from django.core import validators
from django.db import models
from django.urls import reverse

from slugify import slugify

from news_project import settings


class PostApproveManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(status=Post.APPROVE)


class Post(models.Model):
    UNPUBLISHED, APPROVE, DECLINE = 0, 1, 2
    MODERATION_CHOICES = [
        (UNPUBLISHED, 'unpublished'),
        (APPROVE, 'approve'),
        (DECLINE, 'decline'),
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
    status = models.IntegerField(choices=MODERATION_CHOICES, default=0)

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


class PersonalBlog(models.Model):
    author = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    followers = models.ManyToManyField(settings.AUTH_USER_MODEL, blank=True, related_name='blog_followers')
    subscriptions = models.ManyToManyField(settings.AUTH_USER_MODEL, blank=True, related_name='blog_subscriptions')
    read_posts = models.ManyToManyField(Post, blank=True, related_name='blog_read_posts')

    def __str__(self):
        return f'{self.author}'

    def get_absolute_url(self):
        return reverse('user', kwargs={'pk': self.id})
