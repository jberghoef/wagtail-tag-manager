from django.urls import path

from wagtail_tag_manager.views import ManageView
from wagtail_tag_manager.endpoints import lazy_endpoint

app_name = 'wtm'

urlpatterns = [
    path('manage/', ManageView.as_view(), name='manage'),
    path('lazy/', lazy_endpoint, name='lazy')
]
