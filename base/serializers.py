from rest_framework import serializers
from .models import Matchup, PickGroup
from django.contrib.auth import get_user_model
User = get_user_model()


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = [
            'url', 
            'id',
            'username', 
            'email', 
            'following',
            'description',
            'profile_image'
        ]

class MatchupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Matchup
        fields = [
            'url', 
            'id',
            'uid',
            'name', 
            'short_name', 
            'week',
            'year',
            'home_team',
            'away_team',
            'home_score',
            'away_score'
        ]

class PickGroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = PickGroup
        fields = [
            'url', 
            'id',
            'title',
            'owner', 
            'members'
        ]