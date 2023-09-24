from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from . import views


urlpatterns = format_suffix_patterns([
    path('', views.api_root),
    path('users', views.UserListView.as_view(), name='user-list'),
    path('users/<int:pk>', views.UserDetailView.as_view(), name='user-detail'),
    path('matchups', views.MatchupListView.as_view(), name='matchup-list'),
    path('matchups/<int:pk>', views.MatchupDetailView.as_view(), name='matchup-detail'),
    path('groups', views.PickGroupListView.as_view(), name='pickgroup-list'),
    path('groups/<int:pk>', views.PickGroupDetailView.as_view(), name='pickgroup-detail')
])
