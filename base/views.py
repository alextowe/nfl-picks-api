from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.views import FormView, LoginView, LogoutView, PasswordChangeView, PasswordChangeDoneView, PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView, PasswordResetCompleteView
from django.views.generic.edit import FormView, CreateView, UpdateView, DeleteView
from django.views.generic.base import View, TemplateView
from django.contrib import messages
from django.urls import reverse_lazy, reverse
from .models import User
from .forms import RegisterForm, LoginForm, UpdateEmailForm, UpdatePasswordForm, ResetPasswordRequestForm, ResetPasswordForm, DeleteAccountForm

home_page = 'base/index.html'
profile_page = 'base/profile.html'
settings_page = 'base/settings.html'
form_page = 'base/single_form.html'
messages_page = 'base/messages.html'



class RenderTemplate(LoginRequiredMixin, TemplateView):
    """
    Renders a template for an authenticated user.
    """
    template_name = None



class BaseFormView(SuccessMessageMixin, FormView):
    """
    Base form for an unauthenticated user.
    """
    template_name  = form_page
    success_url = 'login'

    def get(self, request):
        if request.user.is_authenticated:
            return redirect('index')
        form = self.get_form()
        return render(request, self.template_name, context={'title': 'Create your account', 'form': form,})
   
    def get_success_url(self):
        """
        Redirects to 'success_url'.
        """
        return reverse_lazy(self.success_url)



class BaseUserFormView(LoginRequiredMixin, SuccessMessageMixin, FormView):
    """
    Base form for an authenticated user. Requires user to be logged in. 
    """
    model = User
    template_name = form_page
    success_url = 'settings'



class SlugUserFormView(BaseUserFormView):
    """
    Form view for url paths containing a slug. Slug defaults to username. Redirects to success_url with the given slug.
    """
    slug_field = 'username'
    success_url = 'settings'
    extra_context = {}

    def get_success_url(self):
        username=self.kwargs['slug']
        return reverse_lazy(self.success_url, kwargs={'slug': username})


class Home(RenderTemplate):
    """
    Renders the home page.
    """
    template_name = home_page



class Profile(RenderTemplate):
    """
    Renders the profile page.
    """
    template_name = profile_page



class Settings(RenderTemplate):
    """
    Renders the settings page.
    """
    template_name = settings_page



class Register(BaseFormView, CreateView):
    """
    Renders the register page to create a new user. 
    """
    form_class = RegisterForm
    success_url = 'login'
    extra_context = {'title': 'Create your account'}
    


class Login(BaseFormView, LoginView):
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



class UpdateEmail(SlugUserFormView, UpdateView):
    """
    Renders the update email page so a user can update their email address.
    """
    form_class = UpdateEmailForm
    extra_context = {'title': 'Update your email address', 'prompt': 'Enter your new email address.'}
    success_message = 'You have successfully updated your email!'
    


class UpdatePassword(SlugUserFormView, PasswordChangeView):
    """
    Renders the update password page so a user can update their password.
    """
    form_class = UpdatePasswordForm
    extra_context = {'title': 'Update your password'}
    success_message = 'You have successfully changed your password!'
    


class ResetPasswordRequest(SlugUserFormView, PasswordResetView):
    """
    Renders the reset password request page to request a password reset link be sent to users email.
    """
    model = User
    form_class = ResetPasswordRequestForm
    email_template_name = 'base/password_reset_email.html'
    extra_context = {'title': 'Password reset request'}
    success_message = 'You have submitted a password reset request! Please check your email for instructions.'
    


class ResetPassword(SlugUserFormView, PasswordResetConfirmView):
    """
    Renders the reset password page so a user can create a new password. Redirects to login page. 
    """
    model = User
    form_class = ResetPasswordForm
    reset_url_token = 'enter-password'
    extra_context = {'title': 'Enter your new password'}
    success_url = 'login'
    success_message = 'You have successfully reset your password! You can now login to your account.'



class DeleteAccount(SlugUserFormView, DeleteView):
    """
    Renders the delete account page so a user can delete their account.
    """
    form_class = DeleteAccountForm
    extra_context = {'title': 'Are you sure? It cannot be recovered.'}
    success_url = reverse_lazy('login')
    success_message = 'You have successfully deleted your account!' 
