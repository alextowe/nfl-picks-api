from django.urls import path
from .views import (
    Home, 
    Register, 
    RegisterComplete,
    InactiveUser,
    Login, 
    Logout, 
    Profile, 
    Settings, 
    UpdateEmail, 
    UpdatePassword, 
    UpdateEmailComplete, 
    UpdatePasswordComplete,
    ResetPasswordRequest, 
    ResetPasswordRequestComplete, 
    ResetPassword, 
    DeleteAccount,
)

urlpatterns = [
    path('', Home.as_view(), name='index'),
    path('register/', Register.as_view(), name='register'),
    path('register/complete/', RegisterComplete.as_view(), name='register-complete'),
    path('login/', Login.as_view(), name='login'),
    path('logout/', Logout.as_view(), name='logout'),
    path('inactive-user/', InactiveUser.as_view(), name='inactive-user'),

    path('profile/<slug>/', Profile.as_view(), name='profile'),
    
    path('settings/<slug>/', Settings.as_view(), name='settings'),
    path('settings/<slug>/update-email/', UpdateEmail.as_view(), name='update-email'),
    path('settings/<slug>/update-email/complete/', UpdateEmailComplete.as_view(), name='update-email-complete'),
    path('settings/<slug>/update-password/', UpdatePassword.as_view(), name='update-password'),
    path('settings/<slug>/update-password/email/', UpdatePasswordComplete.as_view(), name='update-password-done'),
    path('settings/<slug>/delete-account/', DeleteAccount.as_view(), name='delete-account'),

    path('reset-password-request/', ResetPasswordRequest.as_view(), name='reset-password-request'),
    path('reset-password-request/done/', ResetPasswordRequestComplete.as_view(), name='reset-password-request-done'),
    path('reset-password/<uidb64>/<token>/', ResetPassword.as_view(), name='reset-password'),
]
