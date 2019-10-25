from django.db import models
from django.db.models.signals import post_save
from django.contrib.auth.models import User


class BillingProfileManager(models.Manager):
    def new_or_get(self, request):
        obj = None
        created = False
        user = request.user
        if user.is_authenticated:
            obj, created = self.model.objects.get_or_create(user=user)
        return obj, created


class BillingProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    active = models.BooleanField(default=True)
    updated = models.DateTimeField(auto_now=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    # customer_id in stripe

    objects = BillingProfileManager()

    def __str__(self):
        return self.user.email


def user_created_receiver(sender, instance, created, *args, **kwargs):
    if created:
        BillingProfile.objects.get_or_create(user=instance)


post_save.connect(user_created_receiver, sender=User)
