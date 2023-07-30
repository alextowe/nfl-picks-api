# Import tools
from django import forms
from django.forms import (
    CharField,
    EmailField,
)
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _
from django.core.validators import EmailValidator

# Import default forms 
from django.contrib.auth.forms import (
    UserCreationForm, 
    AuthenticationForm, 
    PasswordChangeForm, 
    PasswordResetForm, 
    SetPasswordForm,
)

# Import models
from .models import Profile, FriendRequest
User = get_user_model()



# Base user forms
class EditProfileForm(forms.ModelForm):
    """
    Creates an update profile form. 
    """
    profile_image = forms.FileField(
        widget=forms.ClearableFileInput(
            attrs = {
                'placeholder': 'Display name',
            }
        ), 
        label='Profle picture',
        required=False,
    )

    display_name = forms.CharField(
        widget=forms.TextInput(
            attrs = {
                'placeholder': 'Display name',
            }
        ), 
        label='Display name',
        required=False,
    )

    biography = forms.CharField(
        widget=forms.Textarea(
            attrs = {
                'placeholder': 'Enter a short bio...',
            }
        ), 
        label='Biography',
        required=False,
    )
    
    display_name = forms.CharField(
        widget=forms.TextInput(
            attrs = {
                'placeholder': 'Display name',
            }
        ), 
        label='Display name',
    )

    field_order = ('profile_image', 'display_name', 'biography',)
    
    class Meta:
        model = Profile
        fields = ('profile_image', 'display_name','biography',)

    def __init__(self, *args, **kwargs):
        super(EditProfileForm, self).__init__(*args, **kwargs)

class FriendRequestForm(forms.ModelForm):
    """
    Creates a friend request form. 
    """

    class Meta:
        model = FriendRequest
        exclude = ('request_date', 'is_accepted', 'accepted_on')
        widgets = {
            'from_user': forms.HiddenInput(),
            'to_user': forms.HiddenInput(),
        }

    def __init__(self, *args, **kwargs):
        super(FriendRequestForm, self).__init__(*args, **kwargs)



# User authentication forms
class RegisterForm(UserCreationForm):
    """
    Creates a user creation form. 
    """
    username = forms.CharField(
        widget=forms.TextInput(
            attrs = {
                'placeholder': 'Username',
            }
        ), 
        label='Username',
        error_messages = {
            'required': _('Username is required!'),
            'invalid': _('Invalid Username'),
        }
    )
    
    email = forms.EmailField(widget=forms.EmailInput(
        attrs = {
            'autocomplete':'username', 
            'placeholder': 'Email address',
            }
        ), 
        label='Email address'
    )

    password1 = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                'placeholder': 'Password',
            }
        ), 
        label='Password'
    )

    password2 = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                'placeholder': 'Confirm password',
            }
        ), 
        label='Confirm password'
    )

    field_order = ('username', 'email', 'password1', 'password2')
    
    class Meta:
        model = User        
        fields = ('username', 'email', 'password1', 'password2')

    def save(self, commit=True):
        user = super(RegisterForm, self).save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user
    
class LoginForm(AuthenticationForm):
    """
    Creates a user login form. 
    """
    field_order = ('email', 'password')
    
    email = forms.EmailField(
        widget=forms.EmailInput(
            attrs = {
                'autocomplete':'username', 
                'placeholder': 'Email address',
            }
        ), 
        label='Email address'
    )

    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                'placeholder': 'Password',
            }
        ),
        label='Password'
    )

    class Meta:
        model = User
        fields = ('email', 'password')

    def __init__(self, *args, **kwargs):
        super(LoginForm, self).__init__(*args, **kwargs)
        self.fields.pop('username')



# User settings forms
class UpdateEmailForm(forms.ModelForm):
    """
    Creates an update email form. 
    """
    
    email = forms.EmailField(
        widget=forms.EmailInput(
            attrs = {
            #'autocomplete': 'username', 
            'placeholder': 'Email address',
            }
        ), 
        label='Email address',
        validators=[EmailValidator(message='Invalid Email')],
    )
    
    field_order = ('email',)
    
    class Meta:
        model = User
        fields = ('email',)

    def __init__(self, *args, **kwargs):
        super(UpdateEmailForm, self).__init__(*args, **kwargs)

class UpdatePasswordForm(PasswordChangeForm):
    """
    Creates an update password form. 
    """ 

    old_password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                'autocomplete': 'password',
                'placeholder': 'Current password'
            }
        ), 
        label='Current password'
    )
    
    new_password1 = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                'placeholder': 'New password'
            }
        ), 
        label='New password'
    )
    
    new_password2 = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                'placeholder': 'Confirm new password'
            }
        ), 
        label='Confirm new password'
    )

    class Meta:
        model = User
        fields = ('old_password', 'new_password1', 'new_password2')

    def __init__(self, *args, **kwargs):
        super(UpdatePasswordForm, self).__init__(*args, **kwargs)

class ResetPasswordRequestForm(PasswordResetForm):
    """
    Creates a password reset request form. 
    """
    email = forms.EmailField(widget=forms.EmailInput(
        attrs = {'autocomplete': 'username', 'placeholder': 'Email address'}
    ), label='Email address')

    class Meta:
        model = User
        fields = ('email',)

    def __init__(self, *args, **kwargs):
        super(ResetPasswordRequestForm, self).__init__(*args, **kwargs)

class ResetPasswordForm(SetPasswordForm):
    """
    Creates a password reset form. 
    """
    new_password1 = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                'placeholder': 'Password'
            }
        ), 
        label='Password'
    )
    
    new_password2 = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                'placeholder': 'Confirm password'
            }
        ), 
        label='Confirm password'
    )
    
    class Meta:
        model = User
        fields = ('new_password1', 'new_password2')

    def __init__(self, *args, **kwargs):
        super(ResetPasswordForm, self).__init__(*args, **kwargs)

class DeleteAccountForm(forms.ModelForm):
    """
    Creates a delete account form. 
    """
    class Meta:
        model = User
        fields = ()

    def __init__(self, *args, **kwargs):
        super(DeleteAccountForm, self).__init__(*args, **kwargs)