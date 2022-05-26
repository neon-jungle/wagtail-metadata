

from django.urls import include, path
from wagtail.admin import urls as wagtailadmin_urls
try:
    from wagtail import urls as wagtailadmin_urls
except ImportError:
    from wagtail.core import urls as wagtail_urls

urlpatterns = [
    path('admin/', include(wagtailadmin_urls)),
    path('', include(wagtail_urls)),
]
