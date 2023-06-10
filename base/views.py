# Import tools
from django.shortcuts import render, redirect
from django.contrib.auth import (
    get_user_model, 
    authenticate, 
    login, 
    logout
)

from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
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
    FormMixin,
    FormView, 
    CreateView, 
    UpdateView, 
    DeleteView
)

from django.views.generic import RedirectView 

from django.views.generic.detail import SingleObjectMixin

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

# Import tokens
from .tokens import email_token_generator

# Set page template variables
base_page = 'base/pages/index.html'
home_page = 'base/pages/home.html'
profile_page = 'base/pages/profile.html'
settings_page = 'base/pages/settings.html'
form_page = 'base/pages/form_page.html'
email_verification = 'base/emails/email_verification.html'

# Set user model
User = get_user_model()

# Custom mixins
class RedirectLoggedInMixin(UserPassesTestMixin):
    """
    Redirects an authenticated user. 'test_func' must return false.
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

class EmailVerificationMixin(FormMixin):
    """
    Sends a veriication email to an inactive user on valid form submit.
    """
    subject = 'Verify your email address'
    email_template_name = email_verification
    success_url = None
    success_message = None 
    token_generator = email_token_generator

    def send_verification_email(self, user):
        """
        Sends a verification email to a given user.
        """
        current_site = get_current_site(self.request)
        subject = self.subject
        message = render_to_string(self.email_template_name, {
            'user': user,
            'protocol': 'http',
            'domain': current_site.domain,
            'uid': urlsafe_base64_encode(force_bytes(user.pk)),
            'token': self.token_generator.make_token(user),
        })
        user.email_user(subject, message)

    def form_valid(self, form):
        """
        Sets user to inactive and calls 'send_verification_email'.
        """
        user = form.save(commit=False)
        user.is_active = False
        user.save()

        self.send_verification_email(user)

        messages.success(self.request, self.success_message)
        return redirect(self.success_url)

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
    model = User

class BaseAuthView(RedirectLoggedInMixin, BaseUserFormView):
    """
    Base view used for authentication (login and register).
    """
    redirect_url = 'home' 

class EmailRedirectView(RedirectView):
    """
    Redirects from a email verification link 
    """
    success_message = 'Your email address has been verified!'
    warning_message = 'The verification link was invalid, possibly because it has already been used.'
    token_generator = email_token_generator

    def get(self, request, uidb64, token, *args, **kwargs):
        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None

        if user is not None and self.token_generator.check_token(user, token):
            user.is_active = True
            user.save()
            login(request, user)
            messages.success(request, self.success_message)
        else:
            messages.warning(request, self.warning_message)
        
        return redirect(self.url)

# Basic pages
class Index(UserLoggedOutView):
    """
    Renders the home page.
    """
    redirect_url = 'home'
    template_name = base_page

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
class Register(EmailVerificationMixin, BaseAuthView, CreateView):
    """
    Renders the register page to create a new user. 
    """
    form_class = RegisterForm
    extra_context = {
        'title': 'Register your account',
    }
    success_url = 'login'
    success_message = 'You have successfully created your account! Please check your email for a verification link.'


class Activate(EmailRedirectView):
    """
    Activates a user account. Redirects to login.
    """
    url = 'login'
    
class Login(EmailVerificationMixin, BaseAuthView, LoginView):
    """
    Renders the login page. 
    """
    authentication_form = LoginForm
    form_class = LoginForm
    next_page = 'index' 
    extra_context = {
        'title': 'Login',
    }

    def form_valid(self, form):
        """
        Logs a user in on a POST request. Inactive users cannot login.
        """
        user = authenticate(
            email=form.cleaned_data['email'],
            password=form.cleaned_data['password'],
        )
        if user is not None:
            if user.is_active:
                login(self.request, user) 
                return redirect(self.next_page)
            else:
                self.send_verification_email(user)
                messages.error(self.request, 'Your account has not been verified! Please check your email for a new verification link.') 
        else:
            messages.error(self.request, 'Incorrect email or password!')  
        return redirect('login')

class Logout(LogoutView):
    """
    Logs the current user out.
    """
    next_page = 'login'

class UpdateEmail(EmailVerificationMixin, BaseUserFormView, UpdateView):
    """
    Renders the update email page.
    """
    form_class = UpdateEmailForm
    slug_field = 'username' 
    extra_context = {
        'title': 'Update your email address',
    }
    success_url = reverse_lazy('settings')
    success_message = 'Your email has been updated! Please check your email for a verification link.'

class VerifyEmail(EmailRedirectView):
    """
    Activates a user account. Redirects to login.
    """
    url = 'login'

class UpdatePassword(BaseUserFormView, PasswordChangeView):
    """
    Renders the update password page so a user can update their password.
    """
    form_class = UpdatePasswordForm
    extra_context = {
        'title': 'Update your password'
        
    }
    success_url = reverse_lazy('settings')
    success_message = 'You have successfully changed your password!'

class ResetPasswordRequest(BaseUserFormView, PasswordResetView):
    """
    Renders the reset password request page to request a password reset link be sent to users email. Redirects back to settings.
    """
    form_class = ResetPasswordRequestForm
    email_template_name = 'base/emails/password_reset_email.html'
    title = 'Password reset request'
    success_url = reverse_lazy('settings')
    success_message = 'You have submitted a password reset request! Please check your email for instructions.'

class ResetPassword(BaseUserFormView, PasswordResetConfirmView):
    """
    Renders the reset password page so a user can create a new password. Redirects to login page. 
    """
    model = User
    form_class = ResetPasswordForm
    post_reset_login = True
    reset_url_token = 'reset-password'
    extra_context = {
        'title': 'Enter your new password'
    }
    success_url = reverse_lazy('index')
    success_message = 'You have successfully reset your password! You can now login to your account.'

class DeleteAccount(BaseUserFormView, DeleteView):
    """
    Renders the delete account page so a user can delete their account.
    """
    form_class = DeleteAccountForm
    slug_field = 'username' 
    extra_context = {
        'title': 'Delete your account'
    }
    success_url = reverse_lazy('login')
    success_message = 'You have successfully deleted your account!' 
