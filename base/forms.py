from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, PasswordChangeForm, PasswordResetForm, SetPasswordForm
from.models import User




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
        label='Username'
    )
    
    email = forms.EmailField(widget=forms.EmailInput(
        attrs = {
            'autocomplete':'username', 
            'placeholder': 'Email address',
            }
        ), 
        label='Email address'
    )

    password1 = forms.CharField(widget=forms.PasswordInput(
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
        model = get_user_model()        
        fields = ('username', 'email', 'password1', 'password2')

    def __init__(self, *args, **kwargs):
        super(RegisterForm, self).__init__(*args, **kwargs)
    
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
        model = get_user_model()
        fields = ('email', 'password')

    def __init__(self, *args, **kwargs):
        super(LoginForm, self).__init__(*args, **kwargs)
        self.fields.pop('username')



class UpdateEmailForm(forms.ModelForm):
    """
    Creates an update email form. 
    """
    email = forms.EmailField(
        widget=forms.EmailInput(
            attrs = {
            'autocomplete': 'username', 
            'placeholder': 'Email address',
            }
        ), 
        label='Email address'
    )
    
    field_order = ('email',)
    
    class Meta:
        model = get_user_model()
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
        model = get_user_model()
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
        model = get_user_model()
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
        model = get_user_model()
        fields = ('new_password1', 'new_password2')

    def __init__(self, *args, **kwargs):
        super(ResetPasswordForm, self).__init__(*args, **kwargs)



class DeleteAccountForm(forms.ModelForm):
    """
    Creates a delete account form. 
    """
    class Meta:
        model = get_user_model()
        fields = ()

    def __init__(self, *args, **kwargs):
        super(DeleteAccountForm, self).__init__(*args, **kwargs)
        

