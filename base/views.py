from django.shortcuts import render
from base.permissions import IsOwner, IsOwnerOrReadOnly
from rest_framework.decorators import api_view
from rest_framework import views, generics, mixins, reverse, permissions, status
from base.serializers import UserSerializer, MatchupSerializer, PickGroupSerializer
from rest_framework.response import Response
from rest_framework.reverse import reverse
from .models import Matchup, PickGroup
from django.contrib.auth import get_user_model
User = get_user_model()


@api_view(['GET'])
def api_root(request, format=None):
    return Response({
        'users': reverse('user-list', request=request, format=format),
        'matchups': reverse('matchup-list', request=request, format=format),
        'groups': reverse('pickgroup-list', request=request, format=format)
    })

class UserListView(generics.ListCreateAPIView):
    queryset = User.objects.all().order_by('id')
    serializer_class = UserSerializer

class UserDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all().order_by('id')
    serializer_class = UserSerializer
    permission_classes = [IsOwner]

class MatchupListView(generics.ListAPIView):
    queryset = Matchup.objects.all().order_by('id')
    serializer_class = MatchupSerializer

class MatchupDetailView(generics.RetrieveAPIView):
    queryset = Matchup.objects.all().order_by('id')
    serializer_class = MatchupSerializer


class PickGroupListView(generics.ListCreateAPIView):
    queryset = PickGroup.objects.all().order_by('id')
    serializer_class = PickGroupSerializer

class PickGroupDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = PickGroup.objects.all().order_by('id')
    serializer_class = PickGroupSerializer