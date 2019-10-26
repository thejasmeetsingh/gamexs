from django.db import models
from django.db.models.signals import post_save, pre_save
from django.contrib.auth.models import User
import stripe

stripe.api_key = "sk_test_NriafkzT6rslL62LgZ6yf9UE00lGBuuGIN"


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
    customer_id = models.CharField(max_length=255, blank=True, null=True)

    objects = BillingProfileManager()

    def __str__(self):
        return self.user.email
    
    def charge(self, order_obj, card=None):
        return Charge.objects.do_charge(self, order_obj, card)

    def get_cards(self):
        return self.card_set.all()

    def has_card(self):
        card_qs = self.get_cards()
        return card_qs.exists()

    def default_card(self):
        default_cards = self.get_cards().filter(default=True)
        if default_cards.exists():
            return default_cards.fist()
        return None


class CardManager(models.Manager):
    def add_new(self, billing_profile, token):
        if token:
            customer = stripe.Customer.retrieve(billing_profile.customer_id)
            card_response = customer.sources.create(source=token)
            new_card = self.model(
                billing_profile=billing_profile,
                stripe_id=card_response.id,
                brand=card_response.brand,
                country=card_response.country,
                exp_month=card_response.exp_month,
                exp_year=card_response.exp_year,
                last4=card_response.last4
            )
            new_card.save()
            return new_card
        return None


class Card(models.Model):
    billing_profile = models.ForeignKey(BillingProfile, on_delete=models.CASCADE)
    stripe_id = models.CharField(max_length=255)
    brand = models.CharField(max_length=255, null=True, blank=True)
    country = models.CharField(max_length=255, null=True, blank=True)
    exp_month = models.IntegerField(null=True, blank=True)
    exp_year = models.IntegerField(null=True, blank=True)
    last4 = models.CharField(max_length=4, null=True, blank=True)
    default = models.BooleanField(default=True)

    objects = CardManager()

    def __str__(self):
        return f'{self.brand} {self.last4}'


class ChargeManager(models.Manager):
    def do_charge(self, billing_profile, order_obj, card=None):
        card_obj = card
        if card_obj is None:
            cards = billing_profile.card_set.filter(default=True)
            if cards.exists():
                card_obj = cards.first()
        if card_obj is None:
            return False, "No cards available"

        charge = stripe.Charge.create(
            amount=int(order_obj.total * 100),
            currency='inr',
            customer=billing_profile.customer_id,
            source=card_obj.stripe_id,
            metadata={'order_id': order_obj.order_id},
            description=f'Charge for {billing_profile.user.email}'
        )
        
        new_charge_obj = self.model(
            billing_profile=billing_profile,
            stripe_id=charge.id,
            paid=charge.paid,
            refunded=charge.refunded,
            outcome=charge.outcome,
            outcome_type=charge.outcome['type'],
            seller_message=charge.outcome.get('seller_message'),
            risk_level=charge.outcome.get('risk_level')
        )
        
        new_charge_obj.save()
        return new_charge_obj.paid, new_charge_obj.seller_message


class Charge(models.Model):
    billing_profile = models.ForeignKey(BillingProfile, on_delete=models.CASCADE)
    stripe_id = models.CharField(max_length=255)
    paid = models.BooleanField(default=False)
    refunded = models.BooleanField(default=False)
    outcome = models.TextField(null=True, blank=True)
    outcome_type = models.CharField(max_length=255, null=True, blank=True)
    seller_message = models.CharField(max_length=255, null=True, blank=True)
    risk_level = models.CharField(max_length=255, null=True, blank=True)
    
    objects = ChargeManager()


def billing_profile_created_receiver(sender, instance, *args, **kwargs):
    if not instance.customer_id:
        customer = stripe.Customer.create(
            email=instance.user.email
        )
        instance.customer_id = customer.id


def user_created_receiver(sender, instance, created, *args, **kwargs):
    if created:
        BillingProfile.objects.get_or_create(user=instance)


post_save.connect(user_created_receiver, sender=User)
pre_save.connect(billing_profile_created_receiver, sender=BillingProfile)
