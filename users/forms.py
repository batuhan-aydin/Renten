from django import forms
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm,PasswordResetForm
from django.contrib.auth.models import User



class UserRegisterForm(UserCreationForm):

    class Meta(UserCreationForm.Meta):
        model = User
        fields = UserCreationForm.Meta.fields + ('username', 'email')

class UserLoginForm(AuthenticationForm):
    remember_me = forms.BooleanField(required=False)

class PasswordReset(PasswordResetForm):
    pass

    




