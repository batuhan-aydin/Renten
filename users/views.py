from django.shortcuts import render
from django.http import HttpRequest

# Create your views here.
def register(request):
    return render(request, 'user/register.html')

def login(request):
    return render(request, 'user/login.html')    