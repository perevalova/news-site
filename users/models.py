from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import ugettext_lazy as _
from .managers import CustomUserManager


class CustomUser(AbstractUser):
    """Custom User model"""

    username = None
    email = models.EmailField(_('email address'), unique=True)
    birthday = models.DateField(null=True, blank=True, verbose_name='Birthday')

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()
    def __str__(self):
        return self.email
