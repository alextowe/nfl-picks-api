from .models import Matchup
import requests

def get_matchups():
    url = 'https://site.api.espn.com/apis/site/v2/sports/football/nfl/scoreboard?dates=20181213'
    r = requests.get(url)

    if r.status_code == 200:
        data = r.json()
        events = data['events']
        for event in events:
            duplicate_check = Matchup.objects.get(uid=event['uid'])
            if not duplicate_check:
                matchup = Matchup(
                    uid = event['uid'],
                    name = event['name'],
                    short_name = event['shortName'],
                    week = event['week']['number'],
                    year = event['season']['year'],
                    home_team = event['competitions'][0]['competitors'][0]['team']['name'],
                    away_team = event['competitions'][0]['competitors'][1]['team']['name'],
                )
                matchup.save()           
    return None


def update_score():
    url = 'https://site.api.espn.com/apis/site/v2/sports/football/nfl/scoreboard?dates=20181213'
    r = requests.get(url)

    if r.status_code == 200:
        data = r.json()
        events = data['events']
        for event in events:
            matchup = Matchup.objects.get(uid=event['uid'])
            matchup.home_score = int(event['competitions'][0]['competitors'][0]['score'])
            matchup.away_score = event['competitions'][0]['competitors'][1]['score']
            matchup.save()
        return 