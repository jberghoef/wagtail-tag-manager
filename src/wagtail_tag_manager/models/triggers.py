import re

from django.db import models
from django.forms import widgets
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _
from wagtail.admin.edit_handlers import FieldPanel, MultiFieldPanel

from wagtail_tag_manager.managers import TriggerQuerySet
from wagtail_tag_manager.models.tags import Tag


def searchable_regex_validator(value):
    try:
        re.search(value, "")
    except re.error:
        raise ValidationError(
            "The pattern {pattern} is not valid".format(pattern=value)
        )


class Trigger(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(null=True, blank=True)

    active = models.BooleanField(
        default=True, help_text=_("Uncheck to disable this trigger from firing.")
    )
    pattern = models.CharField(
        max_length=255,
        help_text=_(
            "The regex pattern to match the full url path with. "
            "Groups will be added to the included tag's context."
        ),
        validators=[searchable_regex_validator],
    )
    tags = models.ManyToManyField(
        Tag, help_text=_("The tags to include when this trigger is fired.")
    )

    objects = TriggerQuerySet.as_manager()

    panels = [
        FieldPanel("name", classname="full title"),
        FieldPanel("description", classname="full"),
        MultiFieldPanel(
            [FieldPanel("pattern"), FieldPanel("active")], heading=_("Configuration")
        ),
        FieldPanel("tags", widget=widgets.CheckboxSelectMultiple),
    ]

    def match(self, request):
        if request:
            return re.search(self.pattern, request.get_full_path())
        return False

    def __str__(self):
        return self.name
