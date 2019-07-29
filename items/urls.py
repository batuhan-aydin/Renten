from django.urls import path, include
from items.views import HomeView, ItemDetailView, ItemUpdateView, ItemCreateView, SearchItemView, SearchCategoryView, SearchPriceView

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('item/create/', ItemCreateView.as_view(), name='item-create'),
    path('item/search/', SearchItemView.as_view(), name='search'),
    path('item/category/search', SearchCategoryView.as_view(), name='searchcat'),
    path('item/price/search', SearchPriceView.as_view(), name='search-price'),
    path('item/update/<slug:itemslug>', ItemUpdateView.as_view(), name='item-update'),
    path('item/<slug:itemslug>/', ItemDetailView.as_view(), name='item-detail'),
]
