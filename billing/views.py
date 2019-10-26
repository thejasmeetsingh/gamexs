from django.shortcuts import render
from django.conf import settings
from django.http import JsonResponse, HttpResponse
from django.utils.http import is_safe_url
from django.contrib.auth.decorators import login_required

from .models import BillingProfile, Card

import stripe
STRIPE_SECRET_KEY = getattr(settings, "STRIPE_SECRET_KEY", "sk_test_NriafkzT6rslL62LgZ6yf9UE00lGBuuGIN")
STRIPE_PUB_KEY = getattr(settings, "STRIPE_PUB_KEY", "pk_test_f5DXLBzIlKRIUvm510nNHdd300FSNHSBb3")
stripe.api_key = STRIPE_SECRET_KEY


@login_required
def payment_method_view(request):
    next_url = None
    next_ = request.GET.get('next')
    if is_safe_url(next_, request.get_host()):
        next_url = next_
    return render(request, 'billing/payment_method.html', {"publish_key": STRIPE_PUB_KEY, "next_url": next_url})


@login_required
def payment_method_create_view(request):
    if request.method == 'POST' and request.is_ajax():
        billing_profile, billing_profile_created = BillingProfile.objects.new_or_get(request)
        if not billing_profile:
            return HttpResponse({"message": "Cannot find this user"}, status=401)
        token = request.POST.get('token')
        if token is not None:
            Card.objects.add_new(billing_profile=billing_profile, token=token)
        return JsonResponse({"message": "Success! Your card was added."})
    return HttpResponse("error", status=401)
