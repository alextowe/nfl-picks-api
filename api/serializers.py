import re
from rest_framework import serializers
from rest_framework.utils import model_meta
from api.models import Matchup, PickGroup, Pick
from django.contrib.auth import get_user_model
User = get_user_model()


class PrivateEmailField(serializers.Field):
    """
    Hides the email field in the user serializer if the authenticated user is not owner. 
    """

    def get_attribute(self, instance):
        """
        Passes the user object to the 'to_representation' function.
        """

        return instance

    def to_representation(self, user):
        """
        Returns email if authenticted user matches the object being viewed. 
        """

        if user != self.context['request'].user:
            return ""
        else:
            return user.email

    def to_internal_value(self, data):
        """
        Check the provided email format. 
        """

        regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b'

        if not re.match(regex, data):
            raise serializers.ValidationError('Incorrect format. Expected `name@example.com`.')

        if not isinstance(data, str):
            msg = 'Incorrect type. Expected a string, but got %s'
            raise serializers.ValidationError(msg % type(data).__name__)

        return data

class UserSerializer(serializers.HyperlinkedModelSerializer):
    """
    Serializer for the user model. 
    """

    email = PrivateEmailField()
    password = serializers.CharField(
        style = {'input_type': 'password'},
        write_only = True,
        required = False
    )

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

        return User.objects.create_user(**validated_data)

    def update(self, instance, validated_data):
        """
        Updates a user instance.
        """

        if 'password' in validated_data:
            password = validated_data.pop('password')
            instance.set_password(password)

        return super().update(instance, validated_data)

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
            'completed',
            'winner'
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
            'members',
            'picks_for_group'
        ]
        extra_kwargs = {
            'owner': {'read_only': True}
            
        }

    def create(self, validated_data):
        """
        Creates a new pick group. Sets the authenticated user as the owner and as a member. 
        """

        members = validated_data.pop('members')
        picks_for_group = validated_data.pop('picks_for_group')
        pick_group = PickGroup.objects.create(owner=self.context['request'].user, **validated_data)
        pick_group.members.add(self.context['request'].user, *members)
        
        for matchup in Matchup.active_objects.all():
            pick = Pick.objects.create(owner=self.context['request'].user, pick_group=pick_group, matchup=matchup)

        return pick_group

    def update(self, instance, validated_data):
        """
        Updates a pick group instance.
        """
        
        for member in validated_data['members']:
            for matchup in Matchup.active_objects.all():
                if not Pick.objects.filter(owner=member, pick_group=instance, matchup=matchup).exists():
                    pick = Pick.objects.create(owner=member, pick_group=instance, matchup=matchup)

        return super().update(instance, validated_data)

class PickSerializer(serializers.HyperlinkedModelSerializer):
    """
    Serializer for the pick model. 
    """

    class Meta:
        model = Pick
        fields = [
            'url', 
            'id',
            'owner',
            'pick_group',
            'matchup',
            'selection',
            'is_correct'
        ]
        extra_kwargs = {
            'owner': {'read_only': True},
            'pick_group': {'read_only': True},
            'matchup': {'read_only': True}
        }
