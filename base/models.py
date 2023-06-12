from django.db import models
from django.contrib.auth.models import AbstractUser, PermissionsMixin
from django.utils.translation import gettext_lazy as _
from .managers import UserManager

class User(AbstractUser, PermissionsMixin):
    username = models.CharField(_('username'), unique=True, max_length=50)
    email = models.EmailField(_('email address'), unique=True)
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    objects = UserManager()

    def __str__(self):
        return self.username

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=False, primary_key=True, verbose_name='User profile')
    display_name = models.CharField(default=None, max_length=50)
    biography = models.TextField(blank=True)
    profile_image = models.ImageField(upload_to='photos/profile/', blank=True)

    objects = models.Manager()

    def __str__(self):
        return self.user.username
