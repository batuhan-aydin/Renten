from django.shortcuts import render
from django.views.generic import FormView
from django.contrib.auth.forms import UserCreationForm
from .forms import UserRegisterForm,UserLoginForm,PasswordReset
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset, ButtonHolder, Submit
from django.shortcuts import redirect
from django.contrib.auth.views import LoginView,LogoutView
from django.contrib.auth import login
from django.views.generic.detail import BaseDetailView,DetailView,SingleObjectMixin
from django.conf import settings
from .models import UserProfile
from django.contrib.auth.models import User
class RegistrationView(FormView):
    form_class = UserRegisterForm   
    template_name='user/register.html'
    success_url='/login/'

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)

class Logout(LogoutView):
    next_page = "/"

class Login(LoginView):
    authentication_form = UserLoginForm
    form_class = UserLoginForm
    template_name = 'user/login.html'

    success_url=''
    def form_valid(self, form):
        remember_me = form.cleaned_data['remember_me']
        login(self.request, form.get_user())
        if remember_me:
            self.request.session.set_expiry(1209600)
        return super(LoginView, self).form_valid(form)   

class PasswordResetView(FormView):
    form_class = PasswordReset
    template_name = "user/password_reset.html"
    success_url='/'


class ProfileDetailView(DetailView):
    model = User
    template_name="user/profile.html"
    context_object_name = "object"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["profile"] = UserProfile.objects.filter(user=self.request.user.id)
        return context