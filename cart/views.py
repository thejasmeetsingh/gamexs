from django.shortcuts import render, redirect
from django.core.exceptions import ObjectDoesNotExist
from products.models import Product
from .models import Cart


def cart_home(request):
    try:
        cart_obj = Cart.objects.get(pk=request.session.get('cart_id'))
    except Cart.DoesNotExist:
        cart_obj = False
    if cart_obj:
        return render(request, 'cart/cart_home.html', {'cart': cart_obj})
    else:
        return render(request, 'cart/cart_empty.html')
    

def cart_get_or_create(request):
    product_id = request.POST['product_id']
    if product_id is not None:
        try:
            products_obj = Product.objects.get(id=product_id)
        except ObjectDoesNotExist:
            return redirect('cart_home')
        cart_obj, new_obj = Cart.objects.new_or_get(request)  # get a existing cart or create a new one
        if products_obj in cart_obj.products.all():
            cart_obj.products.remove(products_obj)
        else:
            cart_obj.products.add(products_obj)
    return redirect('cart_home')
