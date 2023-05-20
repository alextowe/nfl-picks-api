from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, PasswordChangeForm
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from.models import User

class RegisterForm(UserCreationForm):
    username = forms.CharField(widget=forms.TextInput(
        attrs = {'placeholder': 'Username'}
    ), label='Username')
    email = forms.EmailField(widget=forms.EmailInput(
        attrs = {'autocomplete':'username', 'placeholder': 'Email address'}
    ), label='Email')
    password1 = forms.CharField(widget=forms.PasswordInput(
        attrs={'placeholder': 'Password'}
    ), label='Password')
    password2 = forms.CharField(widget=forms.PasswordInput(
        attrs={'placeholder': 'Confirm password'}
    ), label='Confirm password')
   
    field_order = ('username', 'email', 'password1', 'password2')
    class Meta:
        model = User        
        fields = ('username', 'email', 'password1', 'password2')

    def __init__(self, *args, **kwargs):
        super(RegisterForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_id = 'id_register_form'
        self.helper.form_class = 'form'
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('register_button', 'Submit', css_class = 'btn btn-dark'))
    
    def save(self, commit=True):
        user = super(RegisterForm, self).save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user

class LoginForm(AuthenticationForm):
    email = forms.EmailField(widget=forms.EmailInput(
        attrs = {'autocomplete': 'username', 'placeholder': 'Email address'}
    ), label='Email address')
    password = forms.CharField(widget=forms.PasswordInput(
        attrs={'placeholder': 'Password'}
    ), label='Password')
    
    field_order = ('email', 'password')
    
    class Meta:
        model = User
        fields = ('email', 'password')

    def __init__(self, *args, **kwargs):
        super(LoginForm, self).__init__(*args, **kwargs)
        self.fields.pop('username')
        self.helper = FormHelper()
        self.helper.form_id = 'id_login_form'
        self.helper.form_class = 'form'
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('bubmit', 'Submit', css_class = 'btn btn-dark'))

class ChangePasswordForm(PasswordChangeForm):
    class Meta:
        model = get_user_model()
        fields = ('old_password', 'new_password1', 'new_password2')

    def __init__(self, *args, **kwargs):
        super(ChangePasswordForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_id = 'id_change_password_form'
        self.helper.form_class = 'form'
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('change_password_button', 'Submit', css_class = 'btn btn-dark'))
