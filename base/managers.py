from django.db import models


class ActiveMatchupManager(models.Manager):

    def get_queryset(self):
        return super().get_queryset().filter(completed=False)

    def get_dates(self):
        return self.get_queryset().dates('date', 'day')

    def get_datetimes(self):
        return self.get_queryset().datetimes('date', 'minute')

    def get_earliest(self, day):
        return self.filter(date__date=day).datetimes('date', 'minute').earliest('date')

    def get_latest(self, day):
        return self.filter(date__date=day).datetimes('date', 'minute').latest('date')

