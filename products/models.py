from django.db import models
import re


class Product(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    category = models.CharField(max_length=10)
    quantity = models.PositiveIntegerField()
    image = models.ImageField(upload_to='images/')
    release_date = models.DateField(auto_now=False)
    price = models.PositiveIntegerField()

    def __str__(self):
        return self.name

    def product_clean_description(self):
        self.description = re.sub('\[\d]', '', self.description)
        return self.description[:358]

    def product_summary(self):
        return self.description[:100]
