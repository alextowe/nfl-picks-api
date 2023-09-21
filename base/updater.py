from datetime import datetime
from apscheduler.schedulers.background import BackgroundScheduler
from . import services

def start():
    scheduler = BackgroundScheduler()
    scheduler.add_job(services.get_matchups, 'interval', minutes=60)
    scheduler.start()