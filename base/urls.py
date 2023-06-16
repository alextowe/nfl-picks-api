from django.urls import path
from .views import (
    Index,
    Home, 
    Register, 
    Activate,
    Login, 
    Logout, 
    ProfileView, 
    EditProfileView,
    Settings, 
    UpdateEmail, 
    VerifyEmail,
    UpdatePassword, 
    ResetPasswordRequest,  
    ResetPassword, 
    DeleteAccount,
)

urlpatterns = [
    path('', Index.as_view(), name='index'),
    path('home/', Home.as_view(), name='home'),
    path('register/', Register.as_view(), name='register'),
    path('activate/<uidb64>/<token>/', Activate.as_view(), name='activate'),
    path('login/', Login.as_view(), name='login'),
    path('logout/', Logout.as_view(), name='logout'),

    path('profile/<slug>/', ProfileView.as_view(), name='profile'),
    path('profile/<slug>/edit/', EditProfileView.as_view(), name='edit-profile'),
    
    path('settings/', Settings.as_view(), name='settings'),
    path('settings/update-email/<slug>/', UpdateEmail.as_view(), name='update-email'),
    path('settings/verify-new-email/<uidb64>/<token>/', VerifyEmail.as_view(), name='verify-new-email'),
    path('settings/update-password/', UpdatePassword.as_view(), name='update-password'),
    path('settings/delete-account/<slug>/', DeleteAccount.as_view(), name='delete-account'),

    path('reset-password-request/', ResetPasswordRequest.as_view(), name='reset-password-request'),
    path('reset-password/<uidb64>/<token>/', ResetPassword.as_view(), name='reset-password'),
]
