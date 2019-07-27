from django.db import models
from django.conf import settings
from products.models import Product

from django.db.models.signals import pre_save, m2m_changed

User = settings.AUTH_USER_MODEL


class CartManager(models.Manager):
    def new_or_get(self, request):
        cart_id = request.session.get('cart_id', None)
        qs = self.get_queryset().filter(id=cart_id)
        if qs.count() == 1:
            new_obj = False
            cart_obj = qs.first()
            if request.user.is_authenticated() and cart_obj.user is None:
                cart_obj.user = request.user
                cart_obj.save()
        else:
            cart_obj = self.new(user=request.user)
            new_obj = True
            request.session['cart_id'] = cart_obj.id
        return cart_obj, new_obj

    def new(self, user=None):
        user_obj = None
        if user is not None:
            if user.is_authenticated():
                user_obj = user
        return self.model.objects.create(user=user_obj)


class Cart(models.Model):
    user = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL)
    products = models.ManyToManyField(Product, blank=True)
    product_quantity = models.PositiveIntegerField()
    sub_total = models.DecimalField(default=0.00, max_digits=100, decimal_places=2)
    total = models.DecimalField(default=0.00, max_digits=100, decimal_places=2)  # total amount of all product
    updated = models.DateTimeField(auto_now=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.id)


def m2m_changed_cart_receiver(sender, instance, action, *args, **kwargs):
    if action == 'post_add' or action == 'post_remove' or action == 'post_clear':
        products = instance.products.all()
        total = 0
        for product in products:
            total += product.price
        if instance.sub_total != total:
            instance.sub_total = total
            instance.save()


def pre_save_cart_receiver(sender, instance, *args, **kwargs):
    instance.total = instance.sub_total * instance.product_quantity


m2m_changed.connect(m2m_changed_cart_receiver, sender=Cart.products.through)
pre_save.connect(pre_save_cart_receiver, sender=Cart)
