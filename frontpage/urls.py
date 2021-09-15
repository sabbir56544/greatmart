from django.urls import path
from .views import home, store, product_detail, cart_view, add_to_cart, remove_cart, remove_cart_item


urlpatterns = [
    path('', home, name='home'),
    path('store', store, name='store'),
    path('store/<slug:category_slug>', store, name='products_by_category'),
    path('<slug:category_slug>/<slug:product_slug>', product_detail, name='products_detail'),
    path('add_to_cart/<int:product_id>/', add_to_cart, name='add_to_cart'),
    path('remove_cart/<int:product_id>/', remove_cart, name='remove_cart'),
    path('remove_cart_item/<int:product_id>/', remove_cart_item, name='remove_cart_item'),
    path('cart', cart_view, name='cart_view'),
]
