from django.db import models
from django.utils import timezone
from datetime import datetime


class ActiveMatchupManager(models.Manager):
    """
    Manager for all matchups that have not been completed.
    """

    def get_queryset(self):
        """
        Filters active matchups by checking for 'completed=False'. 
        """

        return super().get_queryset().filter(completed=False)

    def get_current(self, uid):
        """
        Returns an active matchup for the current day.
        """

        return self.get_queryset().filter(date__date=timezone.make_aware(datetime.now()), uid=uid).first()

    def get_dates(self):
        """
        Returns all dates for active matchups.
        """

        return self.get_queryset().dates('date', 'day')

    def get_datetimes(self):
        """
        Returns all datetimes for active matchups.
        """

        return self.get_queryset().datetimes('date', 'minute')

    def get_earliest(self, day):
        """
        Returns earliest matchup for a given day.
        """

        return self.filter(date__date=day).datetimes('date', 'minute').earliest('date')

    def get_latest(self, day):
        """
        Returns latest matchup for a given day.
        """

        return self.filter(date__date=day).datetimes('date', 'minute').latest('date')

