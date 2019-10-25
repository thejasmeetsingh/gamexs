from django.shortcuts import redirect
from django.utils.http import is_safe_url

from billing.models import BillingProfile
from .forms import AddressForm
from .models import Address


def checkout_address_create_view(request):
    form = AddressForm(request.POST or None)
    context = {
        'form': form
    }
    next_ = request.POST.get('next')
    if form.is_valid():
        instance = form.save(commit=False)
        billing_profile, billing_profile_created = BillingProfile.objects.new_or_get(request)
        if billing_profile is not None:
            address_type = request.POST.get('address_type', 'shipping')
            instance.billing_profile = billing_profile
            instance.address_type = address_type
            instance.save()

            request.session[f'{address_type}_address_id'] = instance.id
        else:
            return redirect('checkout')
        if is_safe_url(next_, request.get_host()):
            return redirect(next_)
    return redirect('checkout')


def checkout_address_reuse_view(request):
    next_ = request.POST.get('next')

    if request.method == 'POST':
        address = request.POST.get('address', None)
        billing_profile, billing_profile_created = BillingProfile.objects.new_or_get(request)
        address_type = request.POST.get('address_type', 'shipping')
        if address is not None:
            qs = Address.objects.filter(billing_profile=billing_profile, id=address)
            if qs.exists():
                request.session[f'{address_type}_address_id'] = address
            if is_safe_url(next_, request.get_host()):
                return redirect(next_)
    return redirect('checkout')
