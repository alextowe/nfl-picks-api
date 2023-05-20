from django.urls import path
from .views import Home, Register, Login, Logout, Profile, Settings, UpdateEmail, UpdatePassword, UpdatePasswordDone, ResetPasswordRequest, ResetPasswordRequestDone, ResetPassword, ResetPasswordComplete, DeleteAccount

urlpatterns = [
    path('', Home.as_view(), name='index'),
    path('register/', Register.as_view(), name='register'),
    path('login/', Login.as_view(), name='login'),
    path('logout/', Logout.as_view(), name='logout'),
    path('<slug>/profile/', Profile.as_view(), name='profile'),
    path('<slug>/settings/', Settings.as_view(), name='settings'),
    path('<slug>/settings/update-email/', UpdateEmail.as_view(), name='update-email'),
    path('<slug>/settings/update-password/', UpdatePassword.as_view(), name='update-password'),
    path('<slug>/settings/update-password/done/', UpdatePasswordDone.as_view(), name='update-password-done'),
    path('<slug>/settings/reset-password-request/', ResetPasswordRequest.as_view(), name='reset-password-request'),
    path('<slug>/settings/reset-password-request/done/', ResetPasswordRequestDone.as_view(), name='reset-password-request-done'),
    path('<slug>/settings/reset-password/<uidb64>/<token>/', ResetPassword.as_view(), name='reset-password'),
    path('<slug>/settings/reset-password/complete', ResetPasswordComplete.as_view(), name='reset-password-complete'),
    path('<slug>/settings/delete-account/', DeleteAccount.as_view(), name='delete-account'),
]
