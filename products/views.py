from django.views import generic as views
from . import models


class ProductListView(views.ListView):
    context_object_name = 'products'
    queryset = models.Product.objects.all().order_by('category')
    template_name = 'products/product_list.html'


class ProductDetailView(views.DetailView):
    context_object_name = 'product'
    model = models.Product
    template_name = 'products/product_detail.html'
