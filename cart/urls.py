from django.urls import path
from . import views

urlpatterns = [
    path('', views.cart_home, name='cart_home'),
    path('update/', views.cart_get_or_create, name='cart_get_or_create')
]
