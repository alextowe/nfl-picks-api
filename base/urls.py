from django.urls import path

from .views import index, home, signup, login_user, logout_user

urlpatterns = [
    path('', index, name='index'),
    path('home/', home, name='home'),
    path('signup/', signup, name='signup'),
    path('login/', login_user, name='login'),
    path('signout/', logout_user, name='logout'),
]
