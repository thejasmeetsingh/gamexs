from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

from products.models import Product
from .models import Cart, Item
from order.models import Order
from billing.models import BillingProfile


def cart_items(request):
    my_cart, new_obj = Cart.objects.new_or_get(request)
    my_cart_items = Item.objects.filter(cart=my_cart)
    return render(request, 'cart/cart.html', {'my_cart': my_cart, 'my_cart_items': my_cart_items})


def cart_create_items(request):
    if request.POST:
        product_id = request.POST.get('product_id')
        product_quantity = int(request.POST.get('product_quantity'))
        my_cart, new_obj = Cart.objects.new_or_get(request)
        product_obj = Product.objects.get(id=product_id)

        if not Item.objects.filter(product=product_obj).exists():
            Item.objects.create(cart=my_cart, product=product_obj, quantity=product_quantity)

        return redirect('cart')


def cart_delete_item(request):
    if request.POST:
        product_id = request.POST.get('item')
        product_obj = Product.objects.get(id=product_id)
        if Item.objects.filter(product=product_obj).exists():
            item_obj = Item.objects.get(product=product_obj)
            item_obj.delete()
        return redirect('cart')


@login_required
def checkout_home(request):
    cart_obj, cart_created = Cart.objects.new_or_get(request)
    order_obj = None
    if cart_created:
        redirect('cart')

    billing_profile, billing_profile_created = BillingProfile.objects.new_or_get(request)

    if billing_profile is not None:
        order_obj, order_obj_created = Order.objects.new_or_get(billing_profile, cart_obj)

    context = {
        'object': order_obj,
        'billing_profile': billing_profile
    }

    return render(request, 'cart/checkout.html', context)
