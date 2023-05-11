from django import forms
from django.contrib.auth.forms import UserCreationForm

from.models import User

class SignUpForm(UserCreationForm):
	class Meta:
		model = User        
		fields = ("username", "email")

def save(self, commit=True):
        user = super(SignUpForm, self).save(commit=False)
        user.email = self.cleaned_data["email"]
        if commit:
            user.save()
        return user

