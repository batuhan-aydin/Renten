from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import DetailView, CreateView, UpdateView,FormView
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
from items.models import Item
from django.contrib.auth.models import User
from django.urls import reverse_lazy
from django.shortcuts import get_object_or_404
from django.db.models import Q


class RegistrationView(FormView):
    form_class = UserRegisterForm   
    template_name='user/register.html'
    success_url='/user/login/'

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


class ProfileDetailView(LoginRequiredMixin,DetailView):
    model = User
    template_name="user/profile.html"
    context_object_name = "profile"
    is_me = False
    def get_object(self, queryset=None):
        if self.is_me:
            return self.request.user
        else:
            return super().get_object(queryset)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["user"] = UserProfile.objects.filter(user=self.request.user)
        context["is_me"] = self.is_me   
        return context
class ProfileUpdateView(LoginRequiredMixin, UpdateView):
    model = UserProfile
    form_class = UserRegisterForm
    def get_success_url(self):
        return reverse_lazy("me")

    def get_object(self, queryset=None):
        return self.request.user

