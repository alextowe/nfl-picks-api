from django.db import models
from django.contrib.auth.models import AbstractUser, PermissionsMixin
from django.utils.translation import gettext_lazy as _
from .managers import UserManager
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.conf import settings
from datetime import datetime

class User(AbstractUser, PermissionsMixin):
    username = models.CharField(_('username'), unique=True, max_length=50)
    email = models.EmailField(_('email address'), unique=True)
    friends = models.ManyToManyField("User", blank=True)
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    objects = UserManager()

    def __str__(self):
        return self.username

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=False, primary_key=True, verbose_name='User profile')
    display_name = models.CharField(null=False, max_length=50)
    biography = models.TextField(blank=True, max_length=150)
    profile_image = models.ImageField(upload_to='base/images/', blank=True)

    @receiver(post_save, sender=User)
    def create_user_profile(sender, instance, created, **kwargs):
        if created:
            Profile.objects.create(user=instance)

    @receiver(post_save, sender=User) 
    def save_user_profile(sender, instance, **kwargs):
        instance.profile.save()

    def save(self, *args, **kwargs):
        """
        Overides the save function to set the default display name to the username. 
        """

        if not self.display_name:
            self.display_name = self.user.username

        super(Profile, self).save(*args, **kwargs)

    def __str__(self):
        return self.user.username


class FriendRequest(models.Model):
    from_user = models.ForeignKey(User, related_name='from_user', on_delete=models.CASCADE, null=True)
    to_user = models.ForeignKey(User, related_name='to_user', on_delete=models.CASCADE, null=True)
    request_date = models.DateTimeField(default=datetime.now)
    is_accepted = models.BooleanField(default=False)
    accepted_on = models.DateTimeField(default=datetime.now)
    is_declined = models.BooleanField(default=False)
    declined_on = models.DateTimeField(default=datetime.now)
    was_canceled = models.BooleanField(default=False)
    canceled_on = models.DateTimeField(default=datetime.now)

