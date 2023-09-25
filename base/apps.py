from django.apps import AppConfig


class BaseConfig(AppConfig):
    """
    Configuration for app: base. 
    """

    default_auto_field = 'django.db.models.BigAutoField'
    name = 'base'
    
    def ready(self):
        """
        Imports the updater module and starts running schedules.
        """
        
        from . import updater
        updater.start_schedules()