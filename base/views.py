from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from .forms import RegistrationForm, LoginForm
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm

from .models import User

def index(request):
    context = {}
    login_form = LoginForm()
    register_form = RegistrationForm()
    template = 'index.html'
    if request.user.is_authenticated:
        template = 'home.html'
    else:
        if request.method == "POST":
            if 'register-button' in request.POST:
                register_form = RegistrationForm(request.POST)
                if register_form.is_valid():
                    user = register_form.save()
                    login(request, user)
                    messages.success(request, "Success! You are now registered!")
                    template = 'home.html'
                else:
                    register_form = RegistrationForm()

            if 'signin-button' in request.POST:
                login_form = LoginForm(request, data=request.POST)
                if login_form.is_valid():
                    email = request.POST['email']
                    password = request.POST['password']
                    user = authenticate(request, email=email, password=password)
                    if user is not None:
                        login(request, user)
                        messages.info(request, f'You are now logged in.')
                        template = 'home.html'
                    else:
                        messages.error(request,'Invalid username or password.')
                else:
                    messages.error(request, "Invalid username or password.")
    context = {
        'register_form': register_form,
        'login_form': login_form,
    }
    return render(request, f'base/{template}', context)

def logout_user(request):
    if request.method == "POST":
        logout(request)
        messages.success(request, 'You are now logged out.')
    return redirect('/')

def profile(request):
    context = {

    }
    return render(request, 'base/profile.html', context)

def settings(request):
    context = {

    }
    return render(request, 'base/settings.html', context)

def delete_user(request, id):
    print(request.method)
    user = User.objects.get(id=id)
    user.delete()
    return redirect('/')
