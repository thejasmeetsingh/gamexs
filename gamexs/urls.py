from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import TemplateView

from search.views import SearchProductView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('products.urls')),
    path('accounts/', include('accounts.urls')),
    path('cart/', include('cart.urls')),
    path('addresses/', include('addresses.urls')),
    path('billing/', include('billing.urls')),
    path('search/', SearchProductView.as_view(), name='search'),
    path('success/', TemplateView.as_view(template_name='success.html'), name='success'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
