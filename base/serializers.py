from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from rest_framework.utils import model_meta
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
    
    def create(self, validated_data):
        ModelClass = self.Meta.model
        info = model_meta.get_field_info(ModelClass)
        many_to_many = {}
        for field_name, relation_info in info.relations.items():
            if relation_info.to_many and (field_name in validated_data):
                many_to_many[field_name] = validated_data.pop(field_name)

        user = User.objects.create_user(**validated_data)
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