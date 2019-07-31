from django import forms
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm,PasswordResetForm,UserChangeForm,ReadOnlyPasswordHashField,ReadOnlyPasswordHashWidget
from django.contrib.auth.models import User
from .models import UserProfile
from django.utils.translation import gettext, gettext_lazy as _
from django.contrib.auth.hashers import (
    UNUSABLE_PASSWORD_PREFIX, identify_hasher,
)
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


class ProfileUpdateForm(UserChangeForm,ReadOnlyPasswordHashField,ReadOnlyPasswordHashWidget):
    password = ReadOnlyPasswordHashField(
        label=_("Password"),
        help_text=_(""),
    )     
    template_name = 'user/profile_edit.html'

  
    class Meta(UserChangeForm):
        model = UserProfile
        fields = [
            'first_name', 'last_name', 'email', 'telephone', 'birth_date', 'location', 'profile_picture']
