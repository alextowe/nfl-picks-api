from django.apps import AppConfig


class APIConfig(AppConfig):
    """
    Configuration for app: api. 
    """

    default_auto_field = 'django.db.models.BigAutoField'
    name = 'api'
    
    def ready(self):
        """
        Imports the updater module and starts running schedules.
        """
        
        from api import schedules
        schedules.start_schedules()