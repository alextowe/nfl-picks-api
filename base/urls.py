from django.urls import path
from .views import Home, Register, Login, Logout, Profile, Settings, UpdateEmail, UpdatePassword, UpdatePasswordDone, ResetPasswordRequest, ResetPasswordRequestDone, ResetPassword, ResetPasswordComplete, DeleteAccount

urlpatterns = [
    path('', Home.as_view(), name='index'),
    path('register/', Register.as_view(), name='register'),
    path('login/', Login.as_view(), name='login'),
    path('logout/', Logout.as_view(), name='logout'),
    path('profile/<slug>/', Profile.as_view(), name='profile'),
    path('settings/<slug>/', Settings.as_view(), name='settings'),
    path('settings/<slug>/update-email/', UpdateEmail.as_view(), name='update-email'),
    path('settings/<slug>/update-password/', UpdatePassword.as_view(), name='update-password'),
    path('settings/<slug>/update-password/done/', UpdatePasswordDone.as_view(), name='update-password-done'),
    path('settings/<slug>/reset-password-request/', ResetPasswordRequest.as_view(), name='reset-password-request'),
    path('settings/<slug>/reset-password-request/done/', ResetPasswordRequestDone.as_view(), name='reset-password-request-done'),
    path('settings/<slug>/reset-password/<uidb64>/<token>/', ResetPassword.as_view(), name='reset-password'),
    path('settings/<slug>/reset-password/complete', ResetPasswordComplete.as_view(), name='reset-password-complete'),
    path('settings/<slug>/delete-account/', DeleteAccount.as_view(), name='delete-account'),
]
