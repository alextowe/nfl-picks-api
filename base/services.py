from .models import Matchup
import requests
from datetime import datetime
from dateutil import parser


def get_matchups():
    url = 'https://site.api.espn.com/apis/site/v2/sports/football/nfl/scoreboard'
    r = requests.get(url)

    if r.status_code == 200:
        data = r.json()
        events = data['events']
        for event in events:
            duplicate_check = Matchup.objects.filter(uid=event['uid'])
            if not duplicate_check:
                matchup = Matchup(
                    uid = event['uid'],
                    name = event['name'],
                    short_name = event['shortName'],
                    week = event['week']['number'],
                    year = event['season']['year'],
                    home_team = event['competitions'][0]['competitors'][0]['team']['name'],
                    away_team = event['competitions'][0]['competitors'][1]['team']['name'],
                    home_score = event['competitions'][0]['competitors'][0]['score'],
                    away_score = event['competitions'][0]['competitors'][1]['score'],
                    date = parser.parse(event['date']),
                    completed = event['status']['type']['completed']
                )
                matchup.save()           


def update_score():
    date = datetime.now().strftime('%Y%m%d')
    url = f'https://site.api.espn.com/apis/site/v2/sports/football/nfl/scoreboard?dates={date}'
    r = requests.get(url)
    
    if r.status_code == 200:
        data = r.json()
        events = data['events']
        for event in events:
            matchup = Matchup.objects.get(uid=event['uid'])
            if not matchup.completed:
                matchup.home_score = event['competitions'][0]['competitors'][0]['score']
                matchup.away_score = event['competitions'][0]['competitors'][1]['score']
                matchup.completed = event['status']['type']['completed']
                matchup.save()
