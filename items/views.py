from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, get_object_or_404
from django.utils import timezone
from django.views.generic.list import ListView
from django.views.generic import DetailView, UpdateView, CreateView
from items.models import Item, Category
from items.forms import ItemCreateForm
from django.db.models import Q

class HomeView(ListView):
    model = Item
    template_name = 'home.html'
    context_object_name = 'items'

    def get_queryset(self):
        queryset = {'all_items': Item.objects.all(), 
                    'all_categories': Category.objects.all()}
        return queryset


class ItemCreateView(CreateView):
    model = Item
    form_class = ItemCreateForm
    template_name = "item/item_create.html"
    success_url = '/'

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super(ItemCreateView, self).form_valid(form)


class ItemUpdateView(LoginRequiredMixin, UpdateView):
    model = Item
    fields = ['name', 'description', 'price', 'picture', 'is_available', 'category']
    template_name = 'item/item_update.html'
    slug_url_kwarg='itemslug'
    success_url = '/'

    def get_object(self):
        item = Item.objects.filter(slug=self.kwargs['itemslug']).first()
        return item

    def get_queryset(self):
        qs = super(ItemUpdateView, self).get_queryset()
        return qs.filter(user=self.request.user)    


class SearchItemView(ListView):
    model = Item
    template_name = "home.html"
    context_object_name = 'items'

    def get_queryset(self):
        query = self.request.GET.get('q')
        
        queryset = {'all_items': Item.objects.filter(Q(name__icontains=query)), 
                    'all_categories': Category.objects.all()}
        return queryset    
   
class SearchCategoryView(ListView):
    model = Item
    template_name = 'home.html'
    context_object_name = 'items'
    def get_queryset(self):
        query = self.request.GET.get('q')
        cat = Category.objects.filter(name=query).first()
        catid = cat.id
        queryset = {'all_items': Item.objects.filter(Q(category=catid)), 
                    'all_categories': Category.objects.all()}
        return queryset    

class SearchPriceView(ListView):
    model = Item
    template_name = 'home.html'
    context_object_name = 'items'

    def get_queryset(self):
        minQuery = self.request.GET.get('minPrice')
        maxQuery = self.request.GET.get('maxPrice')
        queryset = {'all_items': Item.objects.filter(price__range=(minQuery, maxQuery)), 
                    'all_categories': Category.objects.all()
                    }
        return queryset   

class ItemDetailView(LoginRequiredMixin, DetailView):
    model = Item
    template_name = 'item/item_detail.html'
    context_object_name='item'
    slug_url_kwarg='itemslug'
    is_me = False
    # def get_queryset(self):
    #     queryset = super(ItemDetailView, self).get_queryset()
    #     queryset=queryset.filter(
    #         Q(slug=self.kwargs['categoryslug'])|
    #         Q(slug=self.kwargs['itemslug'])
    #     )
    #     return queryset
    def get_object(self, queryset=None):
        if self.is_me:
            return self.request.user
        else:
            return super().get_object(queryset)


    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category'] = Category.objects.filter(Q(slug=self.kwargs['categoryslug']))
        context['itemdetail'] = Item.objects.filter(Q(slug=self.kwargs['itemslug']))
        context["is_me"] = self.is_me
        return context

    # def get_object(self):
    #     obj=self.model.objects.get(
    #     Q(
    #     slug__icontains=self.kwargs['categoryslug']| 
    #     Q(
    #         slug__icontains=self.kwargs['itemslug'])
    #     ))

    #     return obj


