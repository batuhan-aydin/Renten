from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, get_object_or_404
from django.utils import timezone
from django.views.generic.list import ListView
from django.views.generic import DetailView, UpdateView, CreateView, RedirectView
from items.models import Item, Category, ItemRental
from items.forms import ItemCreateForm
from django.urls import reverse
from django.db.models import Q, Prefetch
from django.utils.translation import gettext_noop
from django.http import HttpResponseRedirect

class HomeView(ListView):
    model = Item
    template_name = 'home.html'
    context_object_name = 'items'

    def get_queryset(self):
        queryset = {'all_items': Item.objects.order_by('created_at').filter(is_available=True).all(), 
                    'all_categories': Category.objects.all(),
                    }
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
        
        queryset = {'all_items': Item.objects.filter(Q(name__icontains=query)).order_by('created_at').filter(is_available=True).all(), 
                    'all_categories': Category.objects.all(),
                    'is_search': True}
        return queryset    
   
class SearchCategoryView(ListView):
    model = Item
    template_name = 'home.html'
    context_object_name = 'items'
    def get_queryset(self):
        query = self.request.GET.get('q')
        cat = Category.objects.filter(name=query).first()
        catid = cat.id
        queryset = {'all_items': Item.objects.filter(Q(category=catid)).order_by('created_at').filter(is_available=True).all(), 
                    'all_categories': Category.objects.all(),
                    'is_search': True}
        return queryset    

class SearchPriceView(ListView):
    model = Item
    template_name = 'home.html'
    context_object_name = 'items'

    def get_queryset(self):
        minQuery = self.request.GET.get('minPrice')
        maxQuery = self.request.GET.get('maxPrice')
        queryset = {'all_items': Item.objects.filter(price__range=(minQuery, maxQuery)).order_by('created_at').filter(is_available=True).all(), 
                    'all_categories': Category.objects.all(),
                    'minimum': minQuery,
                    'maximum': maxQuery,
                    'is_search': True
                    }
        return queryset   

class SearchLocationView(ListView):
    model = Item
    template_name = 'home.html'
    context_object_name = 'items'

    def get_queryset(self):
        locationQuery = self.request.GET.get('location')
        queryset = {'all_items': Item.objects.filter(owner__location=locationQuery).order_by('created_at').filter(is_available=True).all(), 
                    'all_categories': Category.objects.all(),
                    'is_search': True
                    }
        return queryset   


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
    # def get_object(self, queryset=None):
    #     if self.is_me:
    #         return self.request.user
    #     else:
    #         return super().get_object(queryset)


    # def get_context_data(self, *args, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     context['category'] = Category.objects.filter(Q(slug=self.kwargs['categoryslug']))
    #     context['itemdetail'] = Item.objects.filter(Q(slug=self.kwargs['itemslug']))
    #     context["is_me"] = self.is_me
    #     return context

    # def get_object(self):
    #     obj=self.model.objects.get(
    #     Q(
    #     slug__icontains=self.kwargs['categoryslug']| 
    #     Q(
    #         slug__icontains=self.kwargs['itemslug'])
    #     ))

    #     return obj

class ItemActionView(RedirectView):
    action = None
    validate = False
    url = None
    context_object_name='item'

    def get_redirect_url(self, *args, **kwargs):
        return self.url or reverse("users:me")

    def apply_action(self, action):
        if action == gettext_noop("rent"):
            ItemRental.objects.create(hirer=self.request.user, item=self.item)
            #self.url= reverse("item-detail", kwargs={'slug':self.kwargs["itemslug"] })
            self.url= reverse("home")
        elif action == gettext_noop("edit"):
            self.url = reverse("item-update", kwargs={"pk": self.item.id})
        elif action == gettext_noop("accept"):
            rental = ItemRental.objects.get(id=self.kwargs["rental_pk"])
            rental.fulfilled = True
            rental.save(update_fields=["fulfilled"])
            rental.item.is_available = False
            rental.item.save(update_fields=["is_available"])
            ItemRental.objects.exclude(id=rental.id).all().delete()
        elif action == gettext_noop("reject"):
            rental = ItemRental.objects.get(id=self.kwargs["rental_pk"])
            rental.delete()
        elif action == gettext_noop("cancel"):
            rental = ItemRental.objects.get(id=self.kwargs["rental_pk"])
            rental.delete()
        elif action == gettext_noop("switchrent"):
            self.item.is_available = not self.item.is_available
            self.item.save(update_fields=["is_available"])
        elif action == gettext_noop("remove"):
            self.item.delete()
        else:
            pass
    


    def get(self, request, *args, **kwargs):
        self.item = Item.objects.get(id=self.kwargs["pk"])
        if self.validate and not request.GET.get("valid") == 'true':
            return render(request, "item/validate.html", {"item": self.item, "action": self.action})
        else:
            self.apply_action(self.action)
            return super().get(request, *args, **kwargs)


class RentListView(LoginRequiredMixin, ListView):
    model = ItemRental
    template_name = 'item/rent_requests.html'
    context_object_name = 'items'
    
    def get_queryset(self):
        queryset = super(RentListView, self).get_queryset()
        queryset = {'all_rents':ItemRental.objects.all().prefetch_related(Prefetch('item', queryset=Item.objects.select_related('owner')))}
        return queryset

