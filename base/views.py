from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import generics, reverse
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.db.models import Q
from base.serializers import UserSerializer, MatchupSerializer, PickGroupSerializer, PickSerializer
from base.permissions import IsOwner, IsOwnerOrReadOnly
from base.models import Matchup, PickGroup, Pick
from django.contrib.auth import get_user_model
User = get_user_model()


@api_view(['GET'])
def api_root(request, format=None):
    """
    View for the API root. Displays list of urls to other views in this API.
    """

    return Response({
        'users': reverse.reverse('user-list', request=request, format=format),
        'matchups': reverse.reverse('matchup-list', request=request, format=format),
        'groups': reverse.reverse('pickgroup-list', request=request, format=format),
        'picks': reverse.reverse('pick-list', request=request, format=format)
    })

class UserListView(generics.ListCreateAPIView):
    """
    List view for user model.
    """

    queryset = User.objects.all().order_by('id')
    serializer_class = UserSerializer
    permission_classes = [AllowAny,]

class UserDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    Detail view for user model.
    """

    queryset = User.objects.all().order_by('id')
    serializer_class = UserSerializer
    permission_classes = [IsOwnerOrReadOnly,]

class MatchupListView(generics.ListAPIView):
    """
    List view for matchup model.
    """
    
    queryset = Matchup.objects.all().order_by('id')
    serializer_class = MatchupSerializer

class MatchupDetailView(generics.RetrieveAPIView):
    """
    Detail view for matchup model.
    """

    queryset = Matchup.objects.all().order_by('id')
    serializer_class = MatchupSerializer


class PickGroupListView(generics.ListCreateAPIView):
    """
    List view for pick group model.
    """

    serializer_class = PickGroupSerializer

    def get_queryset(self):
        """
        Filters pick groups that the authenitcated user is a part of. 
        """

        return PickGroup.objects.filter(
            Q(owner=self.request.user) | 
            Q(members=self.request.user)
        ).order_by('id')

class PickGroupDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    Detail view for pick group model.
    """

    queryset = PickGroup.objects.all().order_by('id')
    serializer_class = PickGroupSerializer
    permission_classes = [IsOwnerOrReadOnly,]

class PickListView(generics.ListCreateAPIView):
    """
    List view for pick model.
    """

    queryset = Pick.objects.all().order_by('id')
    serializer_class = PickSerializer

class PickDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    Detail view for pick model.
    """

    queryset = Pick.objects.all().order_by('id')
    serializer_class = PickSerializer
    permission_classes = [IsOwnerOrReadOnly,]