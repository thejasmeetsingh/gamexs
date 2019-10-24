from django.db import models
from products.models import Product

from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.utils.datetime_safe import datetime
from django.contrib.auth.models import User


class CartManager(models.Manager):
    def new_or_get(self, request):
        cart_id = request.session.get("cart_id", None)
        qs = self.get_queryset().filter(id=cart_id)
        if qs.count() == 1:
            new_obj = False
            cart_obj = qs.first()
            if request.user.is_authenticated and cart_obj.user is None:
                cart_obj.user = request.user
                cart_obj.save()
        else:
            cart_obj = Cart.objects.new(user=request.user)
            new_obj = True
            request.session['cart_id'] = cart_obj.id
        return cart_obj, new_obj

    def new(self, user):
        user_obj = None
        if user is not None:
            if user.is_authenticated:
                user_obj = user
        return self.model.objects.create(user=user_obj)


class Cart(models.Model):
    user = models.ForeignKey(User, null=True, blank=True, on_delete=models.CASCADE)
    total = models.PositiveIntegerField(default=0)
    items = models.PositiveIntegerField(default=0)
    updated = models.DateTimeField(auto_now=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    objects = CartManager()

    def __str__(self):
        return str(self.id)


class Item(models.Model):
    product = models.ForeignKey(Product, null=True, on_delete=models.CASCADE)
    cart = models.ForeignKey(Cart, null=True, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.cart.id} : {self.product.name}"


@receiver(post_save, sender=Item)
def create_cart(sender, instance, **kwargs):
    cost = instance.quantity * instance.product.price
    instance.cart.total += cost
    instance.cart.items += 1
    instance.cart.updated = datetime.now()
    instance.cart.save()


@receiver(post_delete, sender=Item)
def delete_cart(sender, instance, **kwargs):
    cost = instance.quantity * instance.product.price
    instance.cart.total -= cost
    instance.cart.items -= 1
    instance.cart.updated = datetime.now()
    instance.cart.save()
