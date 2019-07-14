from django.views.generic import ListView
from products.models import Product


class SearchProductView(ListView):
    context_object_name = 'products'
    template_name = 'search/search_product.html'
    
    def get_context_data(self, **kwargs):
        context = super(SearchProductView, self).get_context_data(**kwargs)
        context['query'] = self.request.GET.get('q')
        return context

    def get_queryset(self, *args, **kwargs):
        request = self.request
        query = request.GET.get('q', None)
        if query is not None:
            return Product.objects.filter(name__icontains=query)
        return Product.objects.none()
