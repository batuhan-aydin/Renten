from django.shortcuts import render
from django.views.generic import FormView
from .forms import UserRegisterForm

class RegistrationView(FormView):
    form = UserRegisterForm
    template_name='user/register.html'
    success_url='/'

