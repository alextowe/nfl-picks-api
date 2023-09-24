from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password
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
            'password',
            'following',
            'description',
            'profile_image'
        ]
        extra_kwargs = {
            'password': {'write_only': True},
        }

        def validate_password(self, value):
            validate_password(value)
            return value

        def create(self, validated_data):
            user = get_user_model()(**validated_data)

            user.set_password(validated_data['password'])
            user.save()

            return user

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
            'away_score',
            'date',
            'completed'
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