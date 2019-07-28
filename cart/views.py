from django.shortcuts import render, redirect
from django.core.exceptions import ObjectDoesNotExist
from products.models import Product
from .models import Cart


def cart_home(request):
    cart_obj, new_obj = Cart.objects.new_or_get(request)  # get a existing cart or create a new one
    return render(request, 'cart/cart_home.html', {'cart': cart_obj})


def cart_update(request):
    product_id = request.POST['product_id']
    if product_id is not None:
        try:
            products_obj = Product.objects.get(id=product_id)
        except ObjectDoesNotExist:
            return redirect('cart_home')
        cart_obj, new_obj = Cart.objects.new_or_get(request)
        if products_obj in cart_obj.products.all():
            cart_obj.products.remove(products_obj)
        else:
            cart_obj.products.add(products_obj)
    return redirect('cart_home')
