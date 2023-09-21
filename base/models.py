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

class Matchup(models.Model):
    uid = models.CharField(max_length=50)
    name = models.CharField(max_length=50)
    short_name = models.CharField(max_length=50)
    week = models.IntegerField()
    year = models.IntegerField()
    home_team = models.CharField(max_length=50)
    away_team = models.CharField(max_length=50)
    home_score = models.IntegerField(default=0)
    away_score = models.IntegerField(default=0)

    def __str__(self):
        return self.short_name
        