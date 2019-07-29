from django.urls import path, include
from items.views import HomeView, ItemDetailView, ItemUpdateView, ItemCreateView, SearchItemView, SearchCategoryView


urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('item/search/', SearchItemView.as_view(), name='search'),
    path('item/category/search', SearchCategoryView.as_view(), name='searchcat'),
    path('item/create/', ItemCreateView.as_view(), name='item-create'),
    path('item/update/<slug:itemslug>', ItemUpdateView.as_view(), name='item-update'),
    path('item/detail/', ItemDetailView.as_view(is_me=True), name='myitem'),
    path('<slug:categoryslug>/<slug:itemslug>/', ItemDetailView.as_view(), name='item-detail'),
]
