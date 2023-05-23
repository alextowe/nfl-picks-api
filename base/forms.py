from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, PasswordChangeForm, PasswordResetForm, SetPasswordForm
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, ButtonHolder, BaseInput, Submit
from.models import User



class ButtonSubmit(Submit):
    """
    Creates a submit button. 
    """
    input_type = 'submit'
    field_classes = 'btn btn-dark'



class DangerButtonSubmit(ButtonSubmit):
    """
    Creates a danger submit button. 
    """
    field_classes = 'btn btn-outline-danger'



class InputField(BaseInput):
    """
    Creates an instance of an input field. 
    """
    field_classes = '' 
    field_order = ()

    def create_field_list(self):
        for field in self.field_order:
            print(field)



class RegisterForm(UserCreationForm):
    """
    Creates a user creation form. 
    """
    username = forms.EmailField(widget=forms.EmailInput(
        attrs = {'placeholder': 'Username'}
    ), label='Username')
    
    email = forms.EmailField(widget=forms.EmailInput(
        attrs = {'autocomplete':'username', 'placeholder': 'Email address'}
    ), label='Email address')

    password1 = forms.CharField(widget=forms.PasswordInput(
        attrs={'placeholder': 'Password'}
    ), label='Password')

    password2 = forms.CharField(widget=forms.PasswordInput(
        attrs={'placeholder': 'Confirm password'}
    ), label='Confirm password')

    field_order = ('username', 'email', 'password1', 'password2')
    
    class Meta:
        model = get_user_model()        
        fields = ('username', 'email', 'password1', 'password2')

    def __init__(self, *args, **kwargs):
        super(RegisterForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_id = 'id_register_form'
        self.helper.form_class = 'form'
        self.helper.form_method = 'post'
        self.helper.add_input(ButtonSubmit('submit_button', 'Submit'))
    
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
    
    email = forms.EmailField(widget=forms.EmailInput(
        attrs = {'autocomplete':'username', 'placeholder': 'Email address'}
    ), label='Email address')

    password = forms.CharField(widget=forms.PasswordInput(
        attrs={'placeholder': 'Password'}
    ), label='Password')

    class Meta:
        model = get_user_model()
        fields = ('email', 'password')

    def __init__(self, *args, **kwargs):
        super(LoginForm, self).__init__(*args, **kwargs)
        self.fields.pop('username')
        self.helper = FormHelper()
        self.helper.form_id = 'id_login_form'
        self.helper.form_class = 'form'
        self.helper.form_method = 'post'
        self.helper.add_input(ButtonSubmit('submit_button', 'Submit'))



class UpdateEmailForm(forms.ModelForm):
    """
    Creates an update email form. 
    """
    email = forms.EmailField(widget=forms.EmailInput(
        attrs = {'autocomplete': 'username', 'placeholder': 'Email address'}
    ), label='Email address')
    
    field_order = ('email',)
    
    class Meta:
        model = get_user_model()
        fields = ('email',)

    def __init__(self, *args, **kwargs):
        super(UpdateEmailForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_id = 'id_update_email_form'
        self.helper.form_class = 'form'
        self.helper.form_method = 'post'
        self.helper.add_input(ButtonSubmit('update_email_button', 'Submit'))



class UpdatePasswordForm(PasswordChangeForm):
    """
    Creates an update password form. 
    """ 

    old_password = forms.CharField(widget=forms.PasswordInput(
        attrs={'placeholder': 'Current password'}
    ), label='Current password')
    
    new_password1 = forms.CharField(widget=forms.PasswordInput(
        attrs={'placeholder': 'New password'}
    ), label='New password')
    
    new_password2 = forms.CharField(widget=forms.PasswordInput(
        attrs={'placeholder': 'Confirm new password'}
    ), label='Confirm new password')

    class Meta:
        model = get_user_model()
        #fields = ('old_password', 'new_password1', 'new_password2')

    def __init__(self, *args, **kwargs):
        super(UpdatePasswordForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_id = 'id_update_password_form'
        self.helper.form_class = 'form'
        self.helper.form_method = 'post'
        self.helper.add_input(ButtonSubmit('update_password_button', 'Submit'))



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
        self.helper = FormHelper()
        self.helper.form_id = 'id_reset_password_request_form'
        self.helper.form_class = 'form'
        self.helper.form_method = 'post'
        self.helper.add_input(ButtonSubmit('reset_password_request_button', 'Submit'))



class ResetPasswordForm(SetPasswordForm):
    """
    Creates a password reset form. 
    """
    new_password1 = forms.CharField(widget=forms.PasswordInput(
        attrs={'placeholder': 'Password'}
    ), label='Password')
    
    new_password2 = forms.CharField(widget=forms.PasswordInput(
        attrs={'placeholder': 'Confirm password'}
    ), label='Confirm password')
    
    class Meta:
        model = get_user_model()
        fields = ('new_password1', 'new_password2')

    def __init__(self, *args, **kwargs):
        super(ResetPasswordForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_id = 'id_reset_password_form'
        self.helper.form_class = 'form'
        self.helper.form_method = 'post'
        self.helper.add_input(ButtonSubmit('reset_password_button', 'Submit'))



class DeleteAccountForm(forms.ModelForm):
    """
    Creates a delete account form. 
    """
    class Meta:
        model = get_user_model()
        fields = ()

    def __init__(self, *args, **kwargs):
        super(DeleteAccountForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_id = 'id_delete_account_form'
        self.helper.form_class = 'form'
        self.helper.form_method = 'post'
        self.helper.layout = Layout(
            ButtonHolder(
                DangerButtonSubmit('delete_account_button', 'Yes, delete account')
            ),
        )
        

