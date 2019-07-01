from django.db import models


class Product(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    category = models.CharField(max_length=10)
    image = models.ImageField(upload_to='images/')
    release_date = models.DateField(auto_now=False)
    price = models.PositiveIntegerField()

    def __str__(self):
        return self.name
