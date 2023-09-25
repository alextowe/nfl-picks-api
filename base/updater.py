from apscheduler.schedulers.background import BackgroundScheduler
from datetime import timedelta
from .models import Matchup
from .services import get_matchups, update_score


def set_matchup_schedules():
    """
    Creates new a schedule event for every day a matchup takes place. Each event starts at the time of the earliest matchup and ends 5 hours after the start of the last. All events update every 3 minutes. 
    """

    matchups = Matchup.active_objects
    scheduler = BackgroundScheduler()
    scheduler.start()
    
    for day in matchups.get_dates():
        earliest_matchup = matchups.get_earliest(day)
        latest_matchup = matchups.get_latest(day)
        
        scheduler.add_job(
            update_score, 
            'interval',
            start_date=earliest_matchup,
            end_date=latest_matchup + timedelta(hours=5),
            minutes=3
        )

def start_schedules():
    """
    Starts the schedules to get matchups and create schedule events for each day matchups take place. Both events run weekly. 
    """

    scheduler = BackgroundScheduler()
    scheduler.add_job(
        get_matchups, 
        'cron', 
        month='8-12,1-2', 
        day_of_week='wed', 
        hour=5,
        name='get_matchups'
    )
    scheduler.add_job(
        set_matchup_schedules, 
        'cron', 
        day_of_week='wed',
        hour=5,
        minute=15,
        name='update_score'
    )
    scheduler.start()
