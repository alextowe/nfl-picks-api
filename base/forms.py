from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm

from.models import User

class RegistrationForm(UserCreationForm):
    username = forms.CharField(widget=forms.TextInput(
        attrs = {'class': 'form-control', 'placeholder': 'Username'}
    ), label='Username')
    email = forms.EmailField(widget=forms.EmailInput(
        attrs = {'class': 'form-control', 'autocomplete':'username', 'placeholder': 'Email address'}
    ), label='Email')
    password1 = forms.CharField(widget=forms.PasswordInput(
        attrs={'class':'form-control', 'placeholder': 'Password'}
    ), label='Password')
    password2 = forms.CharField(widget=forms.PasswordInput(
        attrs={'class':'form-control', 'placeholder': 'Confirm password'}
    ), label='Confirm password')
    
    class Meta:
        model = User        
        fields = ('username', 'email', 'password1', 'password2')

    def save(self, commit=True):
        user = super(RegistrationForm, self).save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user

class LoginForm(AuthenticationForm):
    email = forms.EmailField(widget=forms.EmailInput(
        attrs = {'class': 'form-control', 'placeholder': 'Email address'}
    ), label='Email address')
    password = forms.CharField(widget=forms.PasswordInput(
        attrs={'class':'form-control', 'placeholder': 'Password'}
    ), label='Password')
    
    class Meta:
        model = User
        fields = ('email', 'password')

    def __init__(self, *args, **kwargs):
        super(LoginForm, self).__init__(*args, **kwargs)
        self.fields.pop('username')
