from django.urls import path
from .views import (
    IndexView,
    HomeView, 

    ProfileView, 
    EditProfileView,
    FriendRequestView,
    FriendsListView,

    RegisterView, 
    ActivateView,
    LoginView, 
    LogoutView, 
    
    SettingsView, 
    UpdateEmailView, 
    VerifyEmailView,
    UpdatePasswordView, 
    ResetPasswordRequestView,  
    ResetPasswordView, 
    DeleteAccountView,
)

urlpatterns = [
    # Base urls
    path('', IndexView.as_view(), name='index'),
    path('home/', HomeView.as_view(), name='home'),

    # Base user urls
    path('profile/<slug>/', ProfileView.as_view(), name='profile'),
    path('profile/<slug>/edit/', EditProfileView.as_view(), name='edit-profile'),
    path('<slug:from_user>/friend-request/<slug:to_user>/', FriendRequestView.as_view(), name='friend-request'),
    path('friends/<slug>/', FriendsListView.as_view(), name='friends'),

    # User auth urls
    path('register/', RegisterView.as_view(), name='register'),
    path('activate/<uidb64>/<token>/', ActivateView.as_view(), name='activate'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    
    # User settings urls
    path('settings/', SettingsView.as_view(), name='settings'),
    path('settings/update-email/<slug>/', UpdateEmailView.as_view(), name='update-email'),
    path('settings/verify-email/<uidb64>/<token>/', VerifyEmailView.as_view(), name='verify-email'),
    path('settings/update-password/', UpdatePasswordView.as_view(), name='update-password'),
    path('settings/delete-account/<slug>/', DeleteAccountView.as_view(), name='delete-account'),
    path('reset-password-request/', ResetPasswordRequestView.as_view(), name='reset-password-request'),
    path('reset-password/<uidb64>/<token>/', ResetPasswordView.as_view(), name='reset-password'),
]
