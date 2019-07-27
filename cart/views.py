from django.shortcuts import render
from .models import Cart


def cart_home(request):
    cart_obj, new_obj = Cart.objects.new_or_get(request)  # get a existing cart or create a new one
    return render(request, 'cart/home.html', cart_obj)
