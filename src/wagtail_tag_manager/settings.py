from django.apps import apps
from django.conf import settings
from django.db import models
from django.utils.translation import ugettext_lazy as _

from wagtail.core.fields import RichTextField
from wagtail.contrib.settings.models import BaseSetting, register_setting


DEFAULT_SETTINGS = {
    "functional": (_("Functional"), "required"),
    "analytical": (_("Analytical"), "initial"),
    "traceable": (_("Traceable"), ""),
}


class TagTypeSettings:
    def __init__(self):
        self.SETTINGS = {}

    @staticmethod
    def all():
        tag_type_settings = getattr(settings, "WTM_TAG_TYPES", DEFAULT_SETTINGS)
        return {
            tag_type: {"verbose_name": config[0], "value": config[1]}
            for tag_type, config in tag_type_settings.items()
        }

    def get(self, tag_type):
        if not tag_type or tag_type not in self.all():
            raise ValueError(_("Provide a valid `tag_type`."))
        return self.all().get(tag_type, "")

    def include(self, value, *args, **kwargs):
        self.SETTINGS.update(
            {
                tag_type: config
                for tag_type, config in self.all().items()
                if config.get("value") == value
            }
        )

        return self

    def exclude(self, value, *args, **kwargs):
        if not self.SETTINGS:
            self.SETTINGS = self.all()

        remove = []
        for tag_type, config in self.SETTINGS.items():
            if config.get("value") == value:
                remove.append(tag_type)

        for item in remove:
            self.SETTINGS.pop(item, None)

        return self

    def result(self):
        return self.SETTINGS


class CookieBarSettings(BaseSetting):
    title = models.CharField(
        max_length=50,
        null=True,
        blank=True,
        help_text=_(
            "The title that should appear on the cookie bar. "
            "Leave empty for the default value."
        ),
    )
    text = RichTextField(
        null=True,
        blank=True,
        help_text=_(
            "The text that should appear on the cookie bar. "
            "Leave empty for the default value."
        ),
    )


if apps.is_installed("wagtail.contrib.settings"):
    register_setting(model=CookieBarSettings)
