from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from .views import (
    api_root,
    UserListView,
    UserDetailView
)

urlpatterns = format_suffix_patterns([
    path('', api_root),
    path('users/', UserListView.as_view(), name='user-list'),
    path('users/<int:pk>/', UserDetailView.as_view(), name='user-detail')
])
