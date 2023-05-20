from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.views import FormView, LoginView, LogoutView, PasswordChangeView, PasswordChangeDoneView, PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView, PasswordResetCompleteView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic.base import TemplateView
from django.contrib import messages
from django.urls import reverse_lazy, reverse
from .models import User
from .forms import RegisterForm, LoginForm, UpdateEmailForm, UpdatePasswordForm, ResetPasswordRequestForm, ResetPasswordForm, DeleteAccountForm

home_page = 'base/index.html'
profile_page = 'base/profile.html'
settings_page = 'base/settings.html'
single_form_page = 'base/single_form.html'
messages_page = 'base/messages.html'



class Home(LoginRequiredMixin, TemplateView):
    template_name = home_page



class Register(CreateView):
    template_name = single_form_page
    form_class = RegisterForm
    success_url = reverse_lazy('login')
    extra_context = {'title': 'Create your account', 'prompt': 'Enter username, email address, and password to create a new account.'}
    
    def get(self, request):
        if request.user.is_authenticated:
            return redirect('index')
        form = self.get_form()
        return render(request, self.template_name, context={'title': 'Create your account', 'form': form,})

 

class Login(LoginView):
    authentication_form = LoginForm
    template_name = single_form_page
    form_class = LoginForm
    next_page = 'index' 
    redirect_authenticated_user = True
    extra_context = {'title': 'Login', 'prompt': 'Login with email and password.'}
    
    def post(self, request):
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



class Logout(LoginRequiredMixin, LogoutView):
    next_page = 'login'



class Profile(LoginRequiredMixin, TemplateView):
    template_name = profile_page



class Settings(LoginRequiredMixin, TemplateView):
    template_name = settings_page



class UpdateEmail(SuccessMessageMixin, UpdateView):
    template_name = single_form_page
    model = User
    form_class = UpdateEmailForm
    slug_field = 'username'
    extra_context = {'title': 'Update your email address', 'prompt': 'Enter your new email address.'}
    success_message = 'You have successfully updated your email!'
    
    def get_success_url(self):
        username=self.kwargs['slug']
        return reverse_lazy('settings', kwargs={'slug': username})



class UpdatePassword(SuccessMessageMixin, PasswordChangeView):
    template_name = single_form_page
    model = User
    form_class = UpdatePasswordForm
    slug_field = 'username'
    extra_context = {'title': 'Update your password', 'prompt': 'Enter your old password first, then enter and confirm your new password.'}
    success_message = 'You have successfully changed your password!'
    
    def get_success_url(self):
        username=self.kwargs['slug']
        return reverse_lazy('update-password-done', kwargs={'slug': username})



class UpdatePasswordDone(PasswordChangeDoneView):
    template_name = settings_page



class ResetPasswordRequest(SuccessMessageMixin, PasswordResetView):
    template_name = single_form_page
    model = User
    form_class = ResetPasswordRequestForm
    email_template_name = 'base/password_reset_email.html'
    slug_field = 'username'
    extra_context = {'title': 'Password reset request', 'prompt': 'Enter your email address to reset your password.'}
    success_message = 'You have submitted a password reset request! Please check your email for instructions.'
    
    def get_success_url(self):
        username=self.kwargs['slug']
        return reverse_lazy('settings', kwargs={'slug': username})



class ResetPasswordRequestDone(PasswordResetDoneView):
    template_name = settings_page



class ResetPassword(SuccessMessageMixin, PasswordResetConfirmView):
    template_name = single_form_page
    model = User
    form_class = ResetPasswordForm
    slug_field = 'username'
    reset_url_token = 'enter-password'
    extra_context = {'title': 'Enter your new password', 'prompt': 'Enter and comfirm your new password.'}
    success_message = 'You have successfully reset your password! Please login to your account.'

    def get_success_url(self):
        username=self.kwargs['slug']
        return reverse_lazy('login')


class ResetPasswordComplete(PasswordResetCompleteView):
    template_name = messages_page



class DeleteAccount(SuccessMessageMixin, DeleteView):
    template_name = single_form_page
    model = User
    form_class = DeleteAccountForm
    slug_field = 'username'
    extra_context = {'title': 'Are you sure?', 'prompt': 'Are you sure you want to delete your account? This action is permanent.'}
    success_url = reverse_lazy('login')
    success_message = 'You have successfully deleted your account!' 
