from django.urls import path
from .views import (
    IndexView,
    HomeView, 
    ProfileView, 
    EditProfileView,
    FriendRequestView,
    FriendRequestsListView,
    AnswerFriendRequestView,
    CancelFriendRequestView,
    FriendsListView,
    SearchForUserView,
    SearchForUserResultsView,
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
    path('send-friend-request/<slug>/', FriendRequestView.as_view(), name='friend-request'),
    path('friend-requests/<slug>/', FriendRequestsListView.as_view(), name='friend-requests-list'),
    path('answer-friend-request/<slug>/', AnswerFriendRequestView.as_view(), name='answer-friend-request'),
    path('cancel-friend-request/<slug>/', CancelFriendRequestView.as_view(), name='cancel-friend-request'),
    path('friends/<slug>/', FriendsListView.as_view(), name='friends'),
    path('search/', SearchForUserView.as_view(), name='search-users'),
    path('add-friend/', SearchForUserResultsView.as_view(), name='add-friend'),
    

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
