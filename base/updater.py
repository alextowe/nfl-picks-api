from apscheduler.schedulers.background import BackgroundScheduler
from datetime import timedelta
from .models import Matchup
from .services import get_matchups, update_score


def get_matchup_days():
    game_dates = Matchup.objects.filter(completed=False).datetimes('date', 'minute')
    scheduler = BackgroundScheduler()
    scheduler.start()

    for day in game_dates.dates('date', 'day'):
        earliest_game = game_dates.filter(date__date=day).earliest('date')
        latest_game = game_dates.filter(date__date=day).latest('date')
        scheduler.add_job(
            update_score, 
            'interval',
            start_date=earliest_game,
            end_date=latest_game + timedelta(hours=5),
            minutes=1
        )

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
        get_matchup_days, 
        'cron', 
        day_of_week='wed',
        hour=5,
        minute=15,
        name='update_score'
    )
    scheduler.start()
