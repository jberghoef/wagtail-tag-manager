from django.urls import path

from .views import lazy_view

app_name = 'wtm'

urlpatterns = [
    path('lazy/', lazy_view, name='lazy')
]
