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
from django.utils.translation import gettext_lazy as _
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_protect
from django.contrib import messages
from datetime import datetime
from django.http import HttpResponseRedirect
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

from django.views.generic import RedirectView, ListView

from django.views.generic.detail import SingleObjectMixin

# Import custom forms 
from .forms import (
    RegisterForm, 
    LoginForm, 
    EditProfileForm,
    FriendRequestForm,
    AnswerFriendRequestForm,
    CancelFriendRequestForm,
    UpdateEmailForm, 
    UpdatePasswordForm,   
    ResetPasswordRequestForm, 
    ResetPasswordForm, 
    DeleteAccountForm
)

# Import models 
from .models import Profile, FriendRequest
User = get_user_model()

# Import token generator
from .tokens import email_token_generator



# Set page templates
BASE_PAGE = 'base/pages/index.html'
HOME_PAGE = 'base/pages/home.html'
PROFILE_PAGE = 'base/pages/profile.html'
FRIENDS_LIST_PAGE = 'base/pages/friends.html'
FRIEND_REQUESTS_PAGE = 'base/pages/friend_requests.html'
ANSWER_FRIEND_REQUEST_FORM = 'base/pages/answer_friend_request.html'
SETTINGS_PAGE = 'base/pages/settings.html'
FORM_PAGE = 'base/pages/form_page.html'
ACCOUNT_VERIFICATION_EMAIL = 'base/emails/email_verification.html'
ACCOUNT_VERIFICATION_SUBJECT = 'base/emails/email_verification_subject.txt'
RESET_PASSWORD_EMAIL = 'base/emails/reset_password.html'
RESET_PASSWORD_SUBJECT = 'base/emails/reset_password_subject.txt'



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

class RedirectWrongUserMixin(UserPassesTestMixin):
    """
    Redirects a user when they try to visit an edit page for another user. 
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
        authorized = False
        if self.request.user.username == self.kwargs['slug']:
            authorized = True
        return authorized

class EmailVerificationMixin(FormMixin):
    """
    Sends a veriication email to an inactive user on valid form submit.
    """
    email_template_name = ACCOUNT_VERIFICATION_EMAIL
    subject = 'Verify your email address'
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
class BaseFormView(SuccessMessageMixin, FormView):
    """
    Base form view.
    """
    template_name = FORM_PAGE


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




# Base pages
class IndexView(RedirectLoggedInMixin, TemplateView):
    """
    Renders the home page.
    """
    redirect_url = 'home'
    template_name = BASE_PAGE

class HomeView(LoginRequiredMixin, SuccessMessageMixin, TemplateView):
    """
    Renders the home page.
    """
    template_name = HOME_PAGE

class ProfileView(LoginRequiredMixin, SuccessMessageMixin, TemplateView):
    """
    Renders the profile page.
    """
    template_name = PROFILE_PAGE
    extra_context = None

    def get_context_data(self, *args, **kwargs):
        """
        """
        context = super(ProfileView, self).get_context_data(**kwargs)
        slug = self.kwargs['slug']
        profile = Profile.objects.filter(user__username=slug)[0]
        profile_friends = profile.user.friends.values_list('username', flat=True)
        mutual_friends = self.request.user.friends.filter(username__in=profile_friends)
        friend_requests = FriendRequest.objects.filter(to_user=self.request.user, is_accepted=False)

        if self.request.user.username in profile_friends:
            context['is_friend'] = True
        else:
            context['is_friend'] = False

        context['profile'] = profile
        context['mutual_friends'] = mutual_friends
        context['friend_requests'] = friend_requests
        return context  

class EditProfileView(SuccessMessageMixin, LoginRequiredMixin, RedirectWrongUserMixin, UpdateView):
    """
    Renders the edit  profile form.
    """
    template_name = FORM_PAGE
    form_class = EditProfileForm 
    model = Profile
    slug_field = 'user__username' 
    redirect_url = 'home'
    extra_context = {
        'title': 'Edit your profile',
    }
    success_message = 'Your profile has been updated!'

    def get_success_url(self):
        """
        """
        username = self.kwargs['slug']
        return reverse_lazy('profile', kwargs={'slug': username})

class FriendRequestView(LoginRequiredMixin, CreateView, BaseUserFormView):
    """
    Renders a form to submit a friend request.
    """
    form_class = FriendRequestForm
    extra_context = {
        'title': 'Add a new friend!',
    }
    model = FriendRequest
    success_url = 'profile'
    success_message = 'You sent a friend request!'

    def get_initial(self, *args, **kwargs):
        """
        """
        from_user = User.objects.filter(username=self.request.user.username)[0]        
        to_user = User.objects.filter(username=self.kwargs['slug'])[0]
        initial = super(FriendRequestView, self).get_initial(**kwargs)
        initial['from_user'] = from_user
        initial['to_user'] = to_user 
        return initial

    def get_success_url(self):
        """
        """
        username = User.objects.filter(username=self.kwargs['slug'])[0]
        return reverse_lazy(self.success_url, kwargs={'slug': username})

class FriendRequestsListView(LoginRequiredMixin, TemplateView):
    """
    """
    template_name = FRIEND_REQUESTS_PAGE
    extra_context = None

    def get_context_data(self, *args, **kwargs):
        """
        """
        context = super(FriendRequestsListView, self).get_context_data(**kwargs)
        user = User.objects.filter(username=self.kwargs['slug'])[0]
        context['friend_requests'] = FriendRequest.objects.filter(
            to_user=user, 
            is_accepted=False, 
            is_declined=False, 
            is_canceled=False
        )
        context['sent_friend_requests'] = FriendRequest.objects.filter(
            from_user=user, 
            is_accepted=False, 
            is_declined=False, 
            is_canceled=False
        )
        return context

class AnswerFriendRequest(LoginRequiredMixin, BaseUserFormView):
    """
    """
    template_name = ANSWER_FRIEND_REQUEST_FORM
    form_class = AnswerFriendRequestForm
    success_url = 'friend-requests-list'
    extra_context = None

    def get_context_data(self, *args, **kwargs):
        """
        """
        context = super(AnswerFriendRequest, self).get_context_data(**kwargs)
        from_user = User.objects.filter(username=self.kwargs['slug'])[0]
        to_user = self.request.user
        context['friend_request'] = FriendRequest.objects.filter(
            from_user=from_user, 
            to_user=to_user, 
            is_accepted=False
        )[0]
        return context

    def get_success_url(self):
        """
        """
        username = self.request.user
        return reverse_lazy(self.success_url, kwargs={'slug': username})

    def post(self, request, *args, **kwargs):
        """
        """
        from_user = User.objects.filter(username=self.kwargs['slug'])[0]
        to_user = self.request.user
        friend_request = FriendRequest.objects.filter(
            from_user=from_user, 
            to_user=to_user, 
            is_accepted=False
        )[0]
        if 'accept-request' in request.POST:
            from_user.friends.add(to_user)
            to_user.friends.add(from_user)
            friend_request.is_accepted = True
            friend_request.is_declined = False
            friend_request.accepted_on = datetime.now()
            from_user.save()
            to_user.save()
            friend_request.save()
        elif'decline-request' in request.POST:
            friend_request.is_accepted = False
            friend_request.is_declined = True
            friend_request.declined_on = datetime.now()
            friend_request.save()

        return HttpResponseRedirect(self.get_success_url())

class CancelFriendRequest(LoginRequiredMixin, BaseUserFormView):
    """
    """
    form_class = CancelFriendRequestForm
    success_url = 'friend-requests-list'
    extra_context = {
        'title': 'Cancel friend request',
    }

    def get_context_data(self, *args, **kwargs):
        """
        """
        context = super(CancelFriendRequest, self).get_context_data(**kwargs)
        from_user = User.objects.filter(username=self.kwargs['slug'])[0]
        to_user = self.request.user
        context['friend_request'] = FriendRequest.objects.filter(
            from_user=from_user, 
            to_user=to_user, 
            is_accepted=False, 
            is_declined=False, 
            is_canceled=False
        )
        return context

    def get_success_url(self):
        """
        """
        username = self.request.user
        return reverse_lazy(self.success_url, kwargs={'slug': username})
    
    def post(self, request, *args, **kwargs):
        """
        """
        from_user = self.request.user
        friend_request = FriendRequest.objects.filter(
            from_user=from_user, 
            is_accepted=False, 
            is_declined=False, 
            is_canceled=False
        )[0]
        friend_request.is_canceled = True
        friend_request.save()
        return HttpResponseRedirect(self.get_success_url())

class FriendsListView(LoginRequiredMixin, TemplateView):
    """
    """
    template_name = FRIENDS_LIST_PAGE
    extra_context = None

    def get_context_data(self, *args, **kwargs):
        """
        """
        context = super(FriendsListView, self).get_context_data(**kwargs)
        user = User.objects.filter(username=self.kwargs['slug'])[0]
        context['user_for_friends_list'] = User.objects.filter(username=user.username)
        return context



# User authentication views
class RegisterView(EmailVerificationMixin, BaseAuthView, CreateView):
    """
    Renders the register page to create a new user. 
    """
    form_class = RegisterForm
    extra_context = {
        'title': 'Register your account',
    }
    success_url = 'login'
    success_message = 'You have successfully created your account! Please check your email for a verification link.'

class ActivateView(EmailRedirectView):
    """
    Activates a user account. Redirects to login.
    """
    url = 'login'
    
class LoginView(EmailVerificationMixin, BaseAuthView, LoginView):
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

class LogoutView(LogoutView):
    """
    Logs the current user out.
    """
    next_page = 'login'



# User settings views
class SettingsView(LoginRequiredMixin, TemplateView):
    """
    Renders the settings page.
    """
    template_name = SETTINGS_PAGE

class UpdateEmailView(LoginRequiredMixin, EmailVerificationMixin, BaseUserFormView, UpdateView):
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

class VerifyEmailView(EmailRedirectView):
    """
    Verifies a new user account. Redirects to login.
    """
    url = 'login'

class UpdatePasswordView(LoginRequiredMixin, BaseUserFormView, PasswordChangeView):
    """
    Renders the update password page so a user can update their password.
    """
    form_class = UpdatePasswordForm
    extra_context = {
        'title': 'Update your password'
        
    }
    success_url = reverse_lazy('settings')
    success_message = 'You have successfully changed your password!'

class ResetPasswordRequestView(BaseUserFormView, PasswordResetView):
    """
    Renders the reset password request page to request a password reset link be sent to users email. Redirects back to settings.
    """
    form_class = ResetPasswordRequestForm
    email_template_name = RESET_PASSWORD_EMAIL
    subject_template_name = RESET_PASSWORD_SUBJECT
    title = 'Password reset request'
    success_url = reverse_lazy('settings')
    success_message = 'You have submitted a password reset request! Please check your email for instructions.'

class ResetPasswordView(BaseUserFormView, PasswordResetConfirmView):
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
    success_message = 'You have reset your password!'

class DeleteAccountView(LoginRequiredMixin, BaseUserFormView, DeleteView):
    """
    Renders the delete account page so a user can delete their account.
    """
    form_class = DeleteAccountForm
    slug_field = 'username' 
    extra_context = {
        'title': 'Delete your account',
        'danger': True
    }
    success_url = reverse_lazy('login')
    success_message = 'You have successfully deleted your account!' 
