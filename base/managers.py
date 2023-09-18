from django.contrib.auth.models import UserManager
from django.db import models


class UserManager(UserManager):
    """
    Manager functions for the User model.
    """

    def get_following(self):
        """
        Returns the 'following' field for a user instance.
        """
        return self.following.all()
    
    def get_followers(self):
        """
        Returns a list of followers for a user instance.
        """
        return self.followers.all()

   

