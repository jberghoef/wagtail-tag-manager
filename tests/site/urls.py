from django.urls import path, include
from wagtail.core import urls as wagtail_urls
from wagtail.admin import urls as wagtailadmin_urls
from django.contrib import admin
from wagtail.documents import urls as wagtaildocs_urls

from wagtail_tag_manager import urls as wtm_urls

urlpatterns = [
    path("admin/", admin.site.urls),
    path("cms/", include(wagtailadmin_urls)),
    path("documents/", include(wagtaildocs_urls)),
    path("wtm/", include(wtm_urls)),
    path("", include(wagtail_urls)),
]
