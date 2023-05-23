from django.shortcuts import render, redirect
from django.contrib.auth import get_user_model, authenticate, login, logout
from django.contrib.auth.mixins import UserPassesTestMixin, LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.views import FormView, LoginView, LogoutView, PasswordChangeView, PasswordChangeDoneView, PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView, PasswordResetCompleteView
from django.views.generic.edit import FormView, CreateView, UpdateView, DeleteView
from django.views.generic.base import View, TemplateView
from django.contrib import messages
from django.urls import reverse_lazy, reverse
from .models import User
from .forms import RegisterForm, LoginForm, UpdateEmailForm, UpdatePasswordForm, ResetPasswordRequestForm, ResetPasswordForm, DeleteAccountForm
from django.core.exceptions import ImproperlyConfigured


home_page = 'base/index.html'
profile_page = 'base/profile.html'
settings_page = 'base/settings.html'
form_page = 'base/single_form.html'
messages_page = 'base/blank_page.html'



####################
#      Mixins      #
####################

class RedirectLoggedInMixin(UserPassesTestMixin):
    """
    Redirects to 'redirect_url' if user is authenticated.
    """
    
    redirect_url = None

    def get_redirect_url(self):
        redirect_url = self.redirect_url
        if not redirect_url:
            raise ImproperlyConfigured(
                '{0} is missing the redirect_url attribute. Define {0}.redirect_url or override '
                '{0}.get_redirect_url().'.format(self.__class__.__name__)
            )
        return str(redirect_url)

    def handle_no_permission(self):
        return redirect(self.get_redirect_url())

    def test_func(self):
        return not self.request.user.is_authenticated








########################
#      Base Views      #
########################

class UserLoggedOutView(RedirectLoggedInMixin, TemplateView):
    """
    Renders a templates for an unauthenticated user. Redirects logged in users.
    """
    template_name = None


class UserLoggedInView(LoginRequiredMixin, TemplateView):
    """
    Renders a template for an authenticated user. Required users to be logged in.
    """
    template_name = None


class MessageView(LoginRequiredMixin, TemplateView):
    """
    Renders a template for an authenticated user. Required users to be logged in.
    """
    template_name = None

class BaseFormView(SuccessMessageMixin, FormView):
    """
    Base form view.
    """
    template_name = form_page


class BaseUserFormView(BaseFormView):
    """
    Base user form view.
    """
    model = get_user_model()


class BaseAuthView(RedirectLoggedInMixin, BaseUserFormView):
    """
    Base view used for authentication (login and register).
    """
    redirect_url = 'index' 
     











###################
#      Pages      #
###################

class Home(UserLoggedInView):
    """
    Renders the home page.
    """
    template_name = home_page



class Profile(UserLoggedInView):
    """
    Renders the profile page.
    """
    template_name = profile_page



class Settings(UserLoggedInView):
    """
    Renders the settings page.
    """
    template_name = settings_page







############################
#      Authentication      #
############################

# /register/
# /login/
# /logout/
class Register(BaseAuthView, CreateView):
    """
    Renders the register page to create a new user. 
    """
    form_class = RegisterForm
    success_url = 'login'
    extra_context = {'title': 'Create your account'}
    
    def post(self, request):
        """
        Creates a user in on a POST request.
        """
        form = self.get_form()
        if form.is_valid():
            user = authenticate(
                email=form.cleaned_data['email'],
                password=form.cleaned_data['password'],
            )
            if user is not None:
                login(request, user)



class Login(BaseAuthView, LoginView):
    """
    Renders the login page so a user can login. 
    """
    authentication_form = LoginForm
    form_class = LoginForm
    next_page = 'index' 
    extra_context = {'title': 'Login'}
    
    def post(self, request):
        """
        Logs a user in on a POST request.
        """
        form = self.get_form()
        if form.is_valid():
            user = authenticate(
                email=form.cleaned_data['email'],
                password=form.cleaned_data['password'],
            )
            if user is not None:
                login(request, user)
                return redirect('index')
            else: 
                messages.error(request, 'Invalid login credentials!')
        return render(request, self.template_name, context={'title': 'Login', 'form': form,})



class Logout(LogoutView):
    """
    Logs the current user out.
    """
    next_page = 'login'








######################
#      Settings      #
######################

# /settings/update-email/<slug>/
# /settings/update-password/
class UpdateEmail(BaseUserFormView, UpdateView):
    """
    Renders the update email page so a user can update their email address.
    """
    form_class = UpdateEmailForm
    slug_field = 'username'
    success_url = reverse_lazy('settings')
    extra_context = {'title': 'Update your email address', 'prompt': 'Enter your new email address.'}
    success_message = 'You have successfully updated your email!'
    


class UpdatePassword(BaseUserFormView, PasswordChangeView):
    """
    Renders the update password page so a user can update their password.
    """
    form_class = UpdatePasswordForm
    success_url = reverse_lazy('settings')
    extra_context = {'title': 'Update your password'}
    success_message = 'You have successfully changed your password!'
    




############################
#      Reset Password      #
############################

# /password-reset/
# /password-reset/done/
# /password-reset/<uidb64>/<token>/
class ResetPasswordRequest(BaseUserFormView, PasswordResetView):
    """
    Renders the reset password request page to request a password reset link be sent to users email.
    """
    form_class = ResetPasswordRequestForm
    email_template_name = 'base/password_reset_email.html'
    success_url = 'done'
    extra_context = {'title': 'Password reset request'}
    success_message = 'You have submitted a password reset request! Please check your email for instructions.'



class ResetPasswordRequestDone(PasswordResetDoneView):
    """
    Renders the confirmation page of successful password reset request.
    """
    template_name = messages_page



class ResetPassword(PasswordResetConfirmView):
    """
    Renders the reset password page so a user can create a new password. Redirects to login page. 
    """
    model = User
    form_class = ResetPasswordForm
    reset_url_token = 'enter-password'
    extra_context = {'title': 'Enter your new password'}
    success_url = 'login'
    success_message = 'You have successfully reset your password! You can now login to your account.'









############################
#      Delete account      #
############################

# /settings/delete-account/<slug>/
class DeleteAccount(BaseUserFormView, DeleteView):
    """
    Renders the delete account page so a user can delete their account.
    """
    form_class = DeleteAccountForm
    slug_field = 'username'
    extra_context = {'title': 'Are you sure? It cannot be recovered.'}
    success_message = 'You have successfully deleted your account!' 
