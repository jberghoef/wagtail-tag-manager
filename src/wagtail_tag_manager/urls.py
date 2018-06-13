from django.urls import path

from .views import ManageView
from .endpoints import lazy_endpoint

app_name = 'wtm'

urlpatterns = [
    path('manage/', ManageView.as_view(), name='manage'),
    path('lazy/', lazy_endpoint, name='lazy')
]
