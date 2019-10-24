from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from search.views import SearchProductView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('products.urls')),
    path('accounts/', include('accounts.urls')),
    path('cart/', include('cart.urls')),
    path('search/', SearchProductView.as_view(), name='search'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
