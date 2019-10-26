from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.conf import settings

from products.models import Product
from .models import Cart, Item
from order.models import Order
from billing.models import BillingProfile
from addresses.models import Address

from addresses.forms import AddressForm

import stripe
STRIPE_SECRET_KEY = getattr(settings, "STRIPE_SECRET_KEY", "sk_test_NriafkzT6rslL62LgZ6yf9UE00lGBuuGIN")
STRIPE_PUB_KEY = getattr(settings, "STRIPE_PUB_KEY", "pk_test_f5DXLBzIlKRIUvm510nNHdd300FSNHSBb3")
stripe.api_key = STRIPE_SECRET_KEY


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
    items = None
    if cart_created:
        redirect('cart')

    address_form = AddressForm()

    billing_address_id = request.session.get('billing_address_id', None)
    shipping_address_id = request.session.get('shipping_address_id', None)

    billing_profile, billing_profile_created = BillingProfile.objects.new_or_get(request)
    address_qs = None
    has_card = None

    if billing_profile is not None:
        address_qs = Address.objects.filter(billing_profile=billing_profile)
        order_obj, order_obj_created = Order.objects.new_or_get(billing_profile, cart_obj)
        items = Item.objects.filter(cart=cart_obj)
        if shipping_address_id:
            order_obj.shipping_address = Address.objects.get(id=shipping_address_id)
            del request.session['shipping_address_id']
        if billing_address_id:
            order_obj.billing_address = Address.objects.get(id=billing_address_id)
            del request.session['billing_address_id']
        if shipping_address_id or billing_address_id:
            order_obj.save()
        has_card = billing_profile.has_card()

    if request.method == 'POST':
        is_prepared = order_obj.check_done()
        if is_prepared:
            did_charge, charge_msg = billing_profile.charge(order_obj)
            if did_charge:
                order_obj.mark_paid()
                Item.objects.all().delete()
                Cart.objects.all().delete()
                return redirect('success')
            else:
                print(charge_msg)
                return redirect('checkout')

    context = {
        'object': order_obj,
        'items': items,
        'billing_profile': billing_profile,
        'address_form': address_form,
        'addresses': address_qs,
        'has_card': has_card,
        'publish_key': STRIPE_PUB_KEY
    }

    return render(request, 'cart/checkout.html', context)
