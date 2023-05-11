from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from .forms import SignUpForm
from django.contrib import messages


def index(request):
    context = {

    }
	
    return render(request, 'base/index.html', context)


def home(request):
    context = {

    }
	
    return render(request, 'base/home.html', context)

def signup(request):
	# redirect to home page if user is already logged in
	if request.user.is_authenticated:
		return redirect('/')
        
	if request.method == 'POST':
		form = SignUpForm(request.POST)
		if form.is_valid():
			user = form.save()
			login(request, user)
			messages.success(request, "Success! You are now registered!")
			return redirect('/home')
	else:
		form = SignUpForm()
	return render(request, 'base/signup.html', {'form': form})

def login_user(request): 
    if request.method == "POST":
        email = request.POST['email']
        password = request.POST['password']
        user = authenticate(request, email=email, password=password)
        if user is not None:
            login(request, user)
            messages.info(request, f'You are now logged in.')
            return redirect('/home')
        else:
            messages.error(request,'Invalid username or password.')
            return redirect('/login')
    return render(request, 'base/login.html')

def logout_user(request):
    if request.method == "POST":
        logout(request)
        messages.success(request, 'You are now logged out.')
    return redirect('/')
