from apscheduler.schedulers.background import BackgroundScheduler
from datetime import timedelta
from .models import Matchup
from .services import get_matchups, update_score


def set_matchup_schedules():
    matchup_dates = Matchup.objects.filter(completed=False).datetimes('date', 'minute')
    scheduler = BackgroundScheduler()
    scheduler.start()

    for day in matchup_dates.dates('date', 'day'):
        earliest_matchup = matchup_dates.filter(date__date=day).earliest('date')
        latest_matchup = matchup_dates.filter(date__date=day).latest('date')
        scheduler.add_job(
            update_score, 
            'interval',
            start_date=earliest_matchup,
            end_date=latest_matchup + timedelta(hours=5),
            minutes=1
        )

    for t in scheduler.get_jobs():
        print(t)

def start_schedules():
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
