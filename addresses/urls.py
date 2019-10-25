from django.urls import path
from . import views

urlpatterns = [
    path('create/', views.checkout_address_create_view, name='checkout_address'),
    path('reuse/', views.checkout_address_reuse_view, name='checkout_address_reuse'),
]
