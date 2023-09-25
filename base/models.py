from django.db import models
from django.contrib.auth.models import AbstractUser, PermissionsMixin
from django.utils.translation import gettext_lazy as _
from datetime import datetime
from base.managers import ActiveMatchupManager


class User(AbstractUser, PermissionsMixin):
    """
    User model that sets 'username' and 'email' to unique, creates a user following/followers system, and stores profile information. 'email' is also a required field. 
    """

    username = models.CharField(_('username'), unique=True, max_length=50)
    email = models.EmailField(_('email address'), unique=True)
    following = models.ManyToManyField('self', blank=True, symmetrical=False, related_name='followers')
    description = models.TextField(blank=True, max_length=150)
    profile_image = models.ImageField(upload_to='base/images/', blank=True)
    
    REQUIRED_FIELDS = ['email']

    def get_following(self):
        """
        Returns a list of users in 'following' list for a given user.
        """

        return self.following.all()
    
    def get_followers(self):
        """
        Returns a list of users that have a given user in their 'following' list. 
        """

        return self.followers.all()

    def __str__(self):
        return self.username

class Matchup(models.Model):
    """
    Matchup model. Uses a custom manager to work with active matchups. 
    """

    uid = models.CharField(max_length=50)
    name = models.CharField(max_length=50)
    short_name = models.CharField(max_length=50)
    week = models.IntegerField()
    year = models.IntegerField()
    home_team = models.CharField(max_length=50)
    away_team = models.CharField(max_length=50)
    home_score = models.IntegerField()
    away_score = models.IntegerField()
    date = models.DateTimeField(default=datetime.now)
    last_updated = models.DateTimeField(default=datetime.now)
    completed = models.BooleanField(default=False)

    objects = models.Manager()
    active_objects = ActiveMatchupManager()

    def __str__(self):
        return self.short_name

class PickGroup(models.Model):
    """
    PickGroup model. Links to 'User' model for 'owner' and 'members' fields. 
    """

    title = models.CharField(max_length=50)
    owner = models.ForeignKey(User, blank=True, related_name='owner_of', on_delete=models.CASCADE)
    members = models.ManyToManyField(User, blank=True, related_name='pick_groups')

    def __str__(self):
        return self.title