from django.urls import path
from .views import LoginUser, HomeView, logout_user
from .forms import LoginForm
urlpatterns = [
    path('', HomeView.as_view(), name='index'),
    path('login/', LoginUser.as_view(), name='login'),
    path('logout/', logout_user, name='logout'),
]
