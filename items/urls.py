from django.urls import path, include
from items.views import HomeView


urlpatterns = [
    path('', HomeView.as_view(), name='home'),
]
