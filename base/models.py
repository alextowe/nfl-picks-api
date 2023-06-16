from django.db import models
from django.contrib.auth.models import AbstractUser, PermissionsMixin
from django.utils.translation import gettext_lazy as _
from .managers import UserManager
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.conf import settings
from datetime import datetime

DEFAULT_PROFILE_IMAGE = f'..{settings.STATIC_URL}base/profile_picture.jpg'

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
    profile_image = models.ImageField(upload_to='photos/profile/', default=DEFAULT_PROFILE_IMAGE)

    @receiver(post_save, sender=User)
    def create_user_profile(sender, instance, created, **kwargs):
        if created:
            Profile.objects.create(user=instance)

    @receiver(post_save, sender=User) 
    def save_user_profile(sender, instance, **kwargs):
        instance.profile.save()

    def save(self, *args, **kwargs):
        self.display_name = self.user.username
        super(Profile, self).save(*args, **kwargs)
    
    def set_image_to_default(self):
        self.profile_image.delete(save=False)
        self.profile_image = DEFAULT_PROFILE_IMAGE
        self.save()

    def __str__(self):
        return self.user.username

class FriendRequest(models.Model):
    from_user = models.ForeignKey(User, related_name='from_user', on_delete=models.CASCADE)
    to_user = models.ForeignKey(User, related_name='to_user', on_delete=models.CASCADE)
    request_date = models.DateTimeField(default=datetime.now)
