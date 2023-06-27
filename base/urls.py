from django.urls import path
from .views import (
    IndexView,
    HomeView, 
    RegisterView, 
    ActivateView,
    LoginView, 
    LogoutView, 
    ProfileView, 
    EditProfileView,
    FriendsListView,
    FriendRequestView,
    SettingsView, 
    UpdateEmailView, 
    VerifyEmailView,
    UpdatePasswordView, 
    ResetPasswordRequestView,  
    ResetPasswordView, 
    DeleteAccountView,
)

urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('home/', HomeView.as_view(), name='home'),
    path('register/', RegisterView.as_view(), name='register'),
    path('activate/<uidb64>/<token>/', ActivateView.as_view(), name='activate'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),

    path('profile/<slug>/', ProfileView.as_view(), name='profile'),
    path('profile/<slug>/edit/', EditProfileView.as_view(), name='edit-profile'),

    path('friends/<slug>/', FriendsListView.as_view(), name='friends'),
    path('<slug:slug>/add-friend/<slug:to_user>', FriendRequestView.as_view(), name='friend-request'),
    
    path('settings/', SettingsView.as_view(), name='settings'),
    path('settings/update-email/<slug>/', UpdateEmailView.as_view(), name='update-email'),
    path('settings/verify-email/<uidb64>/<token>/', VerifyEmailView.as_view(), name='verify-email'),
    path('settings/update-password/', UpdatePasswordView.as_view(), name='update-password'),
    path('settings/delete-account/<slug>/', DeleteAccountView.as_view(), name='delete-account'),

    path('reset-password-request/', ResetPasswordRequestView.as_view(), name='reset-password-request'),
    path('reset-password/<uidb64>/<token>/', ResetPasswordView.as_view(), name='reset-password'),
]
