from django.db import models
from django.conf import settings
from django.dispatch import receiver
from django.core.cache import cache
from django.utils.html import mark_safe
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _
from wagtail.admin.edit_handlers import FieldPanel, FieldRowPanel, MultiFieldPanel


class Constant(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(null=True, blank=True)

    key = models.SlugField(
        max_length=255,
        unique=True,
        help_text=mark_safe(
            _(
                "The key that can be used in tags to include the value.<br/>"
                "For example: <code>{{ ga_id }}</code>."
            )
        ),
    )
    value = models.CharField(
        max_length=255,
        help_text=_("The value to be rendered when this constant is included."),
    )

    panels = [
        FieldPanel("name", classname="full title"),
        FieldPanel("description", classname="full"),
        MultiFieldPanel(
            [FieldRowPanel([FieldPanel("key"), FieldPanel("value")])], heading=_("Data")
        ),
    ]

    def as_dict(self):
        return {
            "name": self.name,
            "description": self.description,
            "key": self.key,
            "value": self.value,
        }

    def get_value(self):
        return self.value

    @classmethod
    def create_context(cls):
        context = cache.get("wtm_constant_cache", {})

        if not context:
            for constant in cls.objects.all():
                context[constant.key] = constant.get_value()

            timeout = getattr(settings, "WTM_CACHE_TIMEOUT", 60 * 30)
            cache.set("wtm_constant_cache", context, timeout)

        return context

    def clean(self):
        from wagtail_tag_manager.models.variables import Variable

        if Variable.objects.filter(key=self.key).exists():
            raise ValidationError(
                f"A variable with the key '{ self.key }' already exists."
            )
        else:
            super().clean()

    def save(
        self, force_insert=False, force_update=False, using=None, update_fields=None
    ):
        self.full_clean()
        return super().save(force_insert, force_update, using, update_fields)

    def __str__(self):
        return self.name


@receiver(models.signals.post_save, sender=Constant)
def handle_constant_save(sender, **kwargs):
    sender.create_context()  # Update the cache
