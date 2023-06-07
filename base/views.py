# Import tools

from django.shortcuts import render, redirect
from django.contrib.auth import (
    get_user_model, 
    authenticate, 
    login, 
    logout
)

from django.contrib import messages
from django.urls import (
    reverse_lazy, 
    reverse
)

from django.core.exceptions import ImproperlyConfigured
from django.contrib.auth.backends import ModelBackend


# Import mixins

from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.mixins import (
    UserPassesTestMixin, 
    LoginRequiredMixin
)


# Import default views

from django.contrib.auth.views import (
    FormView, 
    LoginView, 
    LogoutView, 
    PasswordChangeView, 
    PasswordChangeDoneView, 
    PasswordResetView, 
    PasswordResetDoneView, 
    PasswordResetConfirmView, 
    PasswordResetCompleteView
)

from django.views.generic.base import (
    View, 
    TemplateView
)

from django.views.generic.edit import (
    FormView, 
    CreateView, 
    UpdateView, 
    DeleteView
)

# Import custom forms 

from .forms import (
    RegisterForm, 
    LoginForm, 
    UpdateEmailForm, 
    UpdatePasswordForm,   
    ResetPasswordRequestForm, 
    ResetPasswordForm, 
    DeleteAccountForm
)


# Set page template variables

home_page = 'base/index.html'
profile_page = 'base/profile.html'
settings_page = 'base/settings.html'
form_page = 'base/single_form.html'
message_page = 'base/message_page.html'


# Custom mixins

class RedirectMixin:
    """
    Redirects to 'redirect_url' 
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


class RedirectLoggedInMixin(RedirectMixin, UserPassesTestMixin):
    """
    Redirects an authenticated user. 'test_func' must return false.
    """
    def test_func(self):
        return not self.request.user.is_authenticated


class MessageMixin:
    """
    Adds a message
    """
    success_message = ''

    def get_success_message(self, cleaned_data):
        return self.success_message % cleaned_data


# Base views

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

class MessageView(TemplateView):
    """
    A view for displaying messages.
    """
    template_name = message_page
    extra_context = {}


# Basic pages

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


# User authentication views

class Register(BaseAuthView, CreateView):
    """
    Renders the register page to create a new user. 
    """
    form_class = RegisterForm
    success_url = 'register-complete'
    extra_context = {
        'title': 'Register your account',
        'subhead': 'Fill out the form below to create your new account!',
    }

    def form_valid(self, form):
        """
        Saves the new user form.
        """
        user = form.save(commit=False)
        user.is_active = False
        user.save()
        email = self.request.POST['email']
        password = self.request.POST['password1']
        user = authenticate(
            email=form.cleaned_data['email'], 
            password=form.cleaned_data['password1'],
        )
        #messages.success(self.request, 'You have successfully created your account. Please check your email for a verification link.')
        return redirect(self.success_url)  

class RegisterComplete(MessageView):
    """
    Displays register complete view.
    """
    extra_context = {
        'title': 'New account created!',
        'message': 'You have successfully created your account. A verification email has been sent your email address. Please click the link in the email to complete the verification process.',
        'link': {
            'class': 'btn btn-dark',
            'text': 'Login now!',
            'url': 'login',
        },
    }

class Login(BaseAuthView, LoginView):
    """
    Renders the login page. 
    """
    authentication_form = LoginForm
    form_class = LoginForm
    next_page = 'index' 
    extra_context = {
        'title': 'Login',
        'subhead': 'Sign in to your account!',
    }

    def post(self, request):
        """
        Logs a user in on a POST request. Allows inactive users to login but redirects to a 
        """
        form = self.get_form()
        if form.is_valid():
            user = authenticate(
                email=form.cleaned_data['email'],
                password=form.cleaned_data['password'],
            )
            if user is not None:
                if user.is_active:
                    login(request, user) 
                    return redirect('index')
                else:
                    # resend confirmation email
                    return redirect('inactive-user')
            else:
                messages.error(request, 'No account was found.')  
        return redirect('login')

class Logout(LogoutView):
    """
    Logs the current user out.
    """
    next_page = 'login'

class InactiveUser(MessageView):
    """
    Displays inactive user page
    """
    extra_context = {
        'title': 'Your email address is not verified!',
        'message': 'You need to verify your email address before you can login. A new verification email has been sent your email address. Please click the link in the email to complete the verification process.',
        'link': {
            'class': 'btn btn-dark',
            'text': 'Back to login',
            'url': 'login',
        },
    }

# User settings views

class UpdateEmail(BaseUserFormView, UpdateView):
    """
    Renders the update email page.
    """
    form_class = UpdateEmailForm
    slug_field = 'username' 
    extra_context = {
        'title': 'Update your email address',
        'subhead': 'Enter your new email address. A confirmation email will be sent to verify the new email.',
    }
    success_url = 'complete'
    success_message = 'You have successfully updated your email! Please check your email for a verification link.'

class UpdatePassword(BaseUserFormView, PasswordChangeView):
    """
    Renders the update password page so a user can update their password.
    """
    form_class = UpdatePasswordForm
    extra_context = {
        'title': 'Update your password',
        'subhead': 'You are required to enter your current password before updating it. If you forgot your password, reset it instead.',
        
    }
    success_url = 'complete'
    success_message = 'You have successfully changed your password!'

class UpdateEmailComplete(MessageView):
    """
    Displays inactive user page
    """

class UpdatePasswordComplete(MessageView):
    """
    Displays inactive user page
    """

class ResetPasswordRequest(BaseUserFormView, PasswordResetView):
    """
    Renders the reset password request page to request a password reset link be sent to users email.
    """
    form_class = ResetPasswordRequestForm
    email_template_name = 'base/password_reset_email.html'
    success_url = 'done'
    extra_context = {'title': 'Password reset request'}
    success_message = 'You have submitted a password reset request! Please check your email for instructions.'

class ResetPasswordRequestComplete(PasswordResetDoneView):
    """
    Renders the confirmation page of successful password reset request.
    """
    template_name = message_page

class ResetPassword(PasswordResetConfirmView):
    """
    Renders the reset password page so a user can create a new password. Redirects to login page. 
    """
    model = get_user_model()
    form_class = ResetPasswordForm
    reset_url_token = 'enter-password'
    extra_context = {'title': 'Enter your new password'}
    success_url = 'login'
    success_message = 'You have successfully reset your password! You can now login to your account.'

class DeleteAccount(BaseUserFormView, DeleteView):
    """
    Renders the delete account page so a user can delete their account.
    """
    form_class = DeleteAccountForm
    slug_field = 'username'
    extra_context = {'title': 'Are you sure? It cannot be recovered.'}
    success_url = reverse_lazy('login')
    success_message = 'You have successfully deleted your account!' 
