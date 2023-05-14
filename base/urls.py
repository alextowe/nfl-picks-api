from django.urls import path

from .views import index, logout_user, profile, settings, delete_user

urlpatterns = [
    path('', index, name='index'),
    path('logout/', logout_user, name='logout'),
    path('profile/', profile, name='profile'),
    path('settings/', settings, name='settings'),
    path('delete/<int:id>', delete_user, name='delete'),
]
