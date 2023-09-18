from django.db import models
from django.contrib.auth.models import AbstractUser, PermissionsMixin
from django.utils.translation import gettext_lazy as _
from .managers import UserManager


class User(AbstractUser, PermissionsMixin):
    username = models.CharField(_('username'), unique=True, max_length=50)
    email = models.EmailField(_('email address'), unique=True)
    following = models.ManyToManyField('self', blank=True, symmetrical=False, related_name='followers')
    description = models.TextField(blank=True, max_length=150)
    profile_image = models.ImageField(upload_to='base/images/', blank=True)
    
    REQUIRED_FIELDS = ['email']

    objects = UserManager()

    def __str__(self):
        return self.username