from rest_framework import serializers
from rest_framework.utils import model_meta
from base.models import Matchup, PickGroup
from django.contrib.auth import get_user_model
User = get_user_model()


class PrivateEmailField(serializers.Field):
    """
    Hides the email field in the user serializer if the authenticated user is not owner. 
    """

    def get_attribute(self, user):
        """
        Passes the user object to the 'to_representation' function.
        """
        return user

    def to_representation(self, user):
        """
        Returns email if authenticted user matches the object being viewed. 
        """
        if user != self.context['request'].user:
            return ""
        else:
            return user.email

class UserSerializer(serializers.HyperlinkedModelSerializer):
    """
    Serializer for the user model. 
    """

    email = PrivateEmailField()
    
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
        """
        Creates a new user based on validated data. Removes the many to many field for 'following' from the validated data.
        """

        ModelClass = self.Meta.model
        info = model_meta.get_field_info(ModelClass)
        many_to_many = {}

        for field_name, relation_info in info.relations.items():
            if relation_info.to_many and (field_name in validated_data):
                many_to_many[field_name] = validated_data.pop(field_name)

        user = User.objects.create_user(**validated_data)
        return user

class MatchupSerializer(serializers.HyperlinkedModelSerializer):
    """
    Serializer for the matchup model. 
    """

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
    """
    Serializer for the pick group model. 
    """

    class Meta:
        model = PickGroup
        fields = [
            'url', 
            'id',
            'title',
            'owner', 
            'members'
        ]