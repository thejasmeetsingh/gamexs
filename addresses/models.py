from django.db import models

from billing.models import BillingProfile

ADDRESS_TYPES = (
    ('billing', 'Billing'),
    ('shipping', 'Shipping')
)


class Address(models.Model):
    billing_profile = models.ForeignKey(BillingProfile, on_delete=models.CASCADE)
    address_type = models.CharField(max_length=255, choices=ADDRESS_TYPES)
    address_line_1 = models.CharField(max_length=255, null=False, blank=False)
    address_line_2 = models.CharField(max_length=255, null=True, blank=True)
    city = models.CharField(max_length=255, null=False, blank=False)
    state = models.CharField(max_length=255, null=False, blank=False)
    postal_or_zip_code = models.CharField(max_length=255, null=False, blank=False)
    country = models.CharField(max_length=255, default='India')

    def __str__(self):
        return str(self.billing_profile)

    def get_address(self):
        return "{line_1} {line_2} {city} {state}-{code} {country}".format(
            line_1=self.address_line_1,
            line_2=self.address_line_2 or '',
            city=self.city,
            state=self.state,
            code=self.postal_or_zip_code,
            country=self.country
        )
