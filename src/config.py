from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _


class WagtailTagManagerConfig(AppConfig):
    label = "wagtail_tag_manager"
    name = "wagtail_tag_manager"
    verbose_name = _("Wagtail Tag Manager")
