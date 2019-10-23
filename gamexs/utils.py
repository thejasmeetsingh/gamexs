import random
import string
from django.utils.text import slugify


def string_generator(size=10, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))


def order_id_generator(instance):
    """Generates a unique Alpha Numeric Order ID"""
    order_new_id = string_generator()
    
    _class = instance.__class__
    qs_exists = _class.objects.filter(order_id=order_new_id).exists()
    if qs_exists:
        return slug_generator(instance) 
    return order_new_id


def slug_generator(instance, new_slug=None):
    """Generates a unique slug"""
    if new_slug is not None:
        slug = new_slug
    else:
        slug = slugify(instance.title)
    
    _class = instance.__class__
    qs_exists = _class.objects.filter(slug=slug).exists()
    if qs_exists:
        new_slug = f'{slug}-{string_generator(size=4)}'
        return slug_generator(instance, new_slug=new_slug)
    return slug
