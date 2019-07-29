from django.shortcuts import render, get_object_or_404
from django.utils import timezone
from django.views.generic.list import ListView
from django.views.generic import DetailView
from items.models import Item, Category

class HomeView(ListView):
    model = Item
    template_name = 'home.html'
    context_object_name = 'items'

    def get_queryset(self):
        queryset = {'all_items': Item.objects.all(), 
                    'all_categories': Category.objects.all()}
        return queryset
from django.db.models import Q
class ItemDetailView(DetailView):
    model = Item
    template_name = 'item/item_detail.html'
    context_object_name='item'
    slug_url_kwarg='itemslug'
    # def get_queryset(self):
    #     queryset = super(ItemDetailView, self).get_queryset()
    #     queryset=queryset.filter(
    #         Q(slug=self.kwargs['categoryslug'])|
    #         Q(slug=self.kwargs['itemslug'])
    #     )
    #     return queryset

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category'] = Category.objects.filter(Q(slug=self.kwargs['categoryslug']))
        context['itemslug'] = Item.objects.filter(Q(slug=self.kwargs['itemslug']))
        return context

    # def get_object(self):
    #     obj=self.model.objects.get(
    #     Q(
    #     slug__icontains=self.kwargs['categoryslug']| 
    #     Q(
    #         slug__icontains=self.kwargs['itemslug'])
    #     ))

    #     return obj