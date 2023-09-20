from django.shortcuts import render
from base.permissions import IsOwner, IsOwnerOrReadOnly
from rest_framework.decorators import api_view
from django.contrib.auth.models import Group
from rest_framework import views, generics, mixins, reverse, permissions, status
from base.serializers import UserSerializer, MatchUpSerializer
from rest_framework.response import Response
from rest_framework.reverse import reverse
from .models import MatchUp
from django.contrib.auth import get_user_model
User = get_user_model()
import requests

@api_view(['GET'])
def api_root(request, format=None):
    return Response({
        'users': reverse('user-list', request=request, format=format)
    })

class UserListView(generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class UserDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsOwner]

class GenerateMatchups(generics.ListAPIView):
    queryset = MatchUp.objects.all()
    serializer_class = MatchUpSerializer
    def get(self, request, format=None):
        results = self.request.query_params.get('type')
        response = {}
        r = requests.get('https://site.api.espn.com/apis/site/v2/sports/football/nfl/scoreboard')
        r_status = r.status_code
   
        if r_status == 200:
            data = r.json()
            week = data['week']
            events = data['events']
            for event in events:
                matchup = MatchUp(
                    name = event['name'],
                    short_name = event['shortName'],
                    week = event['week']['number'],
                    year = event['season']['year'],
                    home_team = event['competitions'][0]['competitors'][0]['team']['name'],
                    away_team = event['competitions'][0]['competitors'][1]['team']['name'],
                )
                matchup.save()           

            response['status'] = 200
            response['message'] = 'success'
            response['events'] = events
        else:
            response['status'] = r.status_code
            response['message'] = 'error'
            response['events'] = {}
        return Response(response)