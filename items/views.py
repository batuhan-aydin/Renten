from django.shortcuts import render
from django.utils import timezone
from django.views.generic.list import ListView
from items.models import Item, Category

class HomeView(ListView):
    model = Item
    template_name = 'home.html'
    context_object_name = 'items'

    def get_queryset(self):
        queryset = {'all_items': Item.objects.all(), 
                    'all_categories': Category.objects.all()}
        return queryset
