from django.urls import path, include
from items.views import HomeView, ItemDetailView, ItemUpdateView, ItemCreateView, SearchItemView, SearchCategoryView, SearchPriceView, ItemActionView

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('item/create/', ItemCreateView.as_view(), name='item-create'),
    path('item/search/', SearchItemView.as_view(), name='search'),
    path('item/category/search', SearchCategoryView.as_view(), name='search_category'),
    path('item/price/search', SearchPriceView.as_view(), name='search_price'),
    path("item/<int:pk>/actions/accept/<int:rental_pk>/", ItemActionView.as_view(action="accept"), name="item_accept"),
    path("item/<int:pk>/actions/rent/", ItemActionView.as_view(action="rent"), name="item_rent"),
    path("item/<int:pk>/actions/switch/", ItemActionView.as_view(action="switch"), name="item_switch"),
    path("item/<int:pk>/edit/", ItemActionView.as_view(action="edit"), name="item_edit"),
    path("item/<int:pk>/remove/", ItemActionView.as_view(action="remove", validate=True), name="item_remove"),
    path('item/update/<slug:itemslug>', ItemUpdateView.as_view(), name='item-update'),
    path('item/<slug:itemslug>/', ItemDetailView.as_view(), name='item-detail'),
]
