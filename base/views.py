from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
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
messages_page = 'base/messages.html'



class RedirectIfLoggedInMixin(UserPassesTestMixin):
    """
    Redirect to 'redirect_url' if 'test_func()' returns False.
    """

    redirect_url = 'index'
    
    def get_redirect_url(self):
        """
        Override this method to override the redirect_url attribute.
        """
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


class LoggedOutMixin(RedirectIfLoggedInMixin, SuccessMessageMixin):
    """
    Mixin for views not requiring user authentication. 
    """



class LoggedInMixin(LoginRequiredMixin, SuccessMessageMixin):
    """
    Mixin for views requiring user authentication. 
    """



class UserLoggedOut(LoggedOutMixin, TemplateView):
    """
    Renders a templates for an unauthenticated user. Redirects logged in users.
    """
    template_name = None



class UserLoggedIn(LoggedInMixin, TemplateView):
    """
    Renders a template for an authenticated user. Required users to be logged in.
    """
    template_name = None



class UserLoggedOutForm(LoggedOutMixin, FormView):
    """
    Base form for an unauthenticated user.
    """
    template_name  = form_page
    redirect_url = 'index'



class UserLoggedInForm(LoginRequiredMixin, SuccessMessageMixin ,FormView):
    """
    Base form for an authenticated user. 
    """
    model = User
    template_name = form_page
    success_url = reverse_lazy('settings')



class Home(UserLoggedIn):
    """
    Renders the home page.
    """
    template_name = home_page



class Profile(UserLoggedIn):
    """
    Renders the profile page.
    """
    template_name = profile_page



class Settings(UserLoggedIn):
    """
    Renders the settings page.
    """
    template_name = settings_page


class Register(UserLoggedOutForm, CreateView):
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



class Login(UserLoggedOutForm, LoginView):
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



class UpdateEmail(UserLoggedInForm, UpdateView):
    """
    Renders the update email page so a user can update their email address.
    """
    form_class = UpdateEmailForm
    slug_field = 'username'
    extra_context = {'title': 'Update your email address', 'prompt': 'Enter your new email address.'}
    success_message = 'You have successfully updated your email!'
    


class UpdatePassword(UserLoggedInForm, PasswordChangeView):
    """
    Renders the update password page so a user can update their password.
    """
    form_class = UpdatePasswordForm
    extra_context = {'title': 'Update your password'}
    success_message = 'You have successfully changed your password!'
    


class ResetPasswordRequest(UserLoggedInForm, PasswordResetView):
    """
    Renders the reset password request page to request a password reset link be sent to users email.
    """
    model = User
    form_class = ResetPasswordRequestForm
    email_template_name = 'base/password_reset_email.html'
    extra_context = {'title': 'Password reset request'}
    success_message = 'You have submitted a password reset request! Please check your email for instructions.'
    


class ResetPasswordRequestDone(TemplateView):
    """
    Renders the confirmation page for reset password request.
    """
    template_name = messages_page 



class ResetPassword(UserLoggedOutForm, PasswordResetConfirmView):
    """
    Renders the reset password page so a user can create a new password. Redirects to login page. 
    """
    model = User
    form_class = ResetPasswordForm
    reset_url_token = 'enter-password'
    extra_context = {'title': 'Enter your new password'}
    success_url = 'login'
    success_message = 'You have successfully reset your password! You can now login to your account.'



class DeleteAccount(UserLoggedInForm, DeleteView):
    """
    Renders the delete account page so a user can delete their account.
    """
    form_class = DeleteAccountForm
    slug_field = 'username'
    extra_context = {'title': 'Are you sure? It cannot be recovered.'}
    success_message = 'You have successfully deleted your account!' 
