from django import forms
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm,PasswordResetForm,UserChangeForm
from django.contrib.auth.models import User
from .models import UserProfile

class RealDateInput(forms.DateInput):
    input_type = "date"


class UserRegisterForm(UserCreationForm):
    class Meta(UserCreationForm):
        model = UserProfile
        fields =UserCreationForm.Meta.fields +  (
        "password1","password2", "email","first_name", "last_name","telephone", "birth_date", "location", "profile_picture")
        widgets = {"birthday": RealDateInput}
class UserLoginForm(AuthenticationForm):
    remember_me = forms.BooleanField(required=False)

class PasswordReset(PasswordResetForm):
    pass

class ProfileUpdateForm(UserChangeForm):
    class Meta(UserChangeForm):
        model = UserProfile
        fields = [
            'first_name', 'last_name', 'email', 'telephone', 'birth_date', 'location', 'profile_picture']
