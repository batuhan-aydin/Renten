from django.urls import path, include
from items.views import HomeView, ItemDetailView


urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('<slug:categoryslug>/<slug:itemslug>/', ItemDetailView.as_view(), name='item-detail'),
]
