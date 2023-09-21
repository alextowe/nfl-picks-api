from django.shortcuts import render
from base.permissions import IsOwner, IsOwnerOrReadOnly
from rest_framework.decorators import api_view
from django.contrib.auth.models import Group
from rest_framework import views, generics, mixins, reverse, permissions, status
from base.serializers import UserSerializer, MatchUpSerializer
from rest_framework.response import Response
from rest_framework.reverse import reverse
from .models import Matchup
from django.contrib.auth import get_user_model
User = get_user_model()
import requests


@api_view(['GET'])
def api_root(request, format=None):
    return Response({
        'users': reverse('user-list', request=request, format=format),
        'matchups': reverse('matchup-list', request=request, format=format)
    })

class UserListView(generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class UserDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsOwner]

class MatchupListView(generics.ListAPIView):
    queryset = Matchup.objects.all()
    serializer_class = MatchUpSerializer
    
    def get(self, request, format=None, *args, **kwargs):
        r = requests.get('https://site.api.espn.com/apis/site/v2/sports/football/nfl/scoreboard')
   
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
                    )
                    matchup.save()           
        return self.list(request, *args, **kwargs)

class MatchupDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Matchup.objects.all()
    serializer_class = MatchUpSerializer