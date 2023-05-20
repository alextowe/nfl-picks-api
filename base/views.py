from django.shortcuts import render, redirect
from django.contrib.auth import logout
from django.contrib.auth.views import LoginView
from django.views.generic.base import TemplateView
from django.contrib import messages
from .models import User
from .forms import RegisterForm, LoginForm

class LoginUser(LoginView):
    authentication_form = LoginForm
    template_name = 'base/login.html'
    next_page = 'index' 
    
    def post(self, request, *args, **kwargs):
        """
        Handle POST requests: instantiate a form instance with the passed
        POST variables and then check if it's valid.
        """
        form = self.get_form()
        print(form)
        if form.is_valid():
            print("Valid")
            print(form.get_user())
            return self.form_valid(form)
        else:
            print("Invalid")
            return self.form_invalid(form)




class HomeView(TemplateView):
    template_name = 'base/home.html'


def logout_user(request):
    if request.method == "POST":
        logout(request)
        messages.success(request, 'You are now logged out.')
    return redirect('/')


