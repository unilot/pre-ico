from django.contrib import admin
from django.conf.urls import url, include
from django.conf.urls.static import static
from django.conf.urls.i18n import i18n_patterns
from . import settings

urlpatterns = [
    url(r'^o2/', include('oauth2_provider.urls', namespace='oauth2_provider')),
    url('admin/', admin.site.urls),
    url(r'^martor/', include('martor.urls')),
]

urlpatterns += i18n_patterns(
    url(r'^cp/', include('cp.urls', namespace='cp')),
    url(r'^coinpayments/', include('coinpayments.urls', namespace='coinpayments')),
    url('', include('django.conf.urls.i18n')),
    url(r'^', include('landing.urls', namespace='landing')),
)

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
