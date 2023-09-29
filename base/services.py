import requests
from django.utils import timezone
from datetime import datetime
from dateutil import parser
from base.models import Matchup, PickGroup, Pick


def get_matchups():
    """
    Gets matchups for the current week and saves them to new matchups instances. 
    """

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

    for group in PickGroup.objects.all():
        for member in group.members.all():
            for matchup in Matchup.active_objects.all():
                if not Pick.objects.filter(owner=member, pick_group=group, matchup=matchup).exists():
                    pick = Pick.objects.create(owner=member, pick_group=group, matchup=matchup)        

def update_score():
    """
    Updates matchup scores for the current day.
    """

    date = timezone.make_aware(datetime.now()).strftime('%Y%m%d')
    url = f'https://site.api.espn.com/apis/site/v2/sports/football/nfl/scoreboard?dates={date}'
    r = requests.get(url)
    
    if r.status_code == 200:
        data = r.json()
        events = data['events']
        for event in events:
            matchup = Matchup.active_objects.get_current(event['uid'])
            if matchup:
                matchup.home_score = event['competitions'][0]['competitors'][0]['score']
                matchup.away_score = event['competitions'][0]['competitors'][1]['score']
                matchup.last_updated = timezone.make_aware(datetime.now())
                matchup.completed = event['status']['type']['completed']

                if matchup.completed:
                    if matchup.home_score > matchup.away_score:
                        matchup.winner = '1'
                    elif matchup.home_score < matchup.away_score:
                        matchup.winner = '2'

                    for pick in Pick.objects.filter(matchup=matchup):
                        if pick.selection == "":
                            print("No Selection")  
                        elif pick.selection == matchup.winner:
                            pick.is_correct = True
                            pick.save()  

                matchup.save()     

            
