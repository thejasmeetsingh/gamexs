from django.urls import path
from . import views

urlpatterns = [
    path('', views.cart_items, name='cart'),
    path('your-cart/', views.cart_create_items, name='cart_create_item'),
    path('delete-cart-item/', views.cart_delete_item, name='cart_delete_item'),
    path('checkout/', views.checkout_home, name='checkout')
]
