from django import forms
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm,PasswordResetForm
from django.contrib.auth.models import User
from .models import UserProfile


class UserRegisterForm(UserCreationForm):
    birth_date = forms.DateField(help_text='Required. Format: YYYY-MM-DD',required=False)
    telephone = forms.CharField(max_length=30,required=False)
    location = forms.CharField(max_length=50,required=False)
    profile_picture = forms.ImageField(required=False)   
    class Meta(UserCreationForm.Meta):
        model = User
        fields =UserCreationForm.Meta.fields +  ("username","password1","password2","email","first_name","last_name","telephone","location","birth_date","profile_picture")        
class UserLoginForm(AuthenticationForm):
    remember_me = forms.BooleanField(required=False)

class PasswordReset(PasswordResetForm):
    pass

class ProfileUpdateForm(forms.ModelForm):
    pass
    # class Meta(UserProfile.Meta):
    #     model = UserProfile
    #     fields = UserCreationForm.Meta.fields + (
    #     'telephone', 'location', 'profil_picture')        

