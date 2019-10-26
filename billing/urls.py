from django.urls import path
from . import views

urlpatterns = [
    path('payment/', views.payment_method_view, name='payment_method'),
    path('payment/create/', views.payment_method_create_view, name='payment_create'),
]
