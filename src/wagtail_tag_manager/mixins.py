from django.db import models
from django.forms import widgets
from django.utils.translation import ugettext_lazy as _
from wagtail.admin.edit_handlers import FieldPanel, MultiFieldPanel, PublishingPanel
from wagtail.utils.decorators import cached_classmethod

from wagtail_tag_manager.models import Tag


class TagMixin(models.Model):
    tags = models.ManyToManyField(
        Tag, help_text=_("The tags to include when this page is loaded.")
    )

    settings_panels = [
        PublishingPanel(),
        MultiFieldPanel(
            [FieldPanel("tags", widget=widgets.CheckboxSelectMultiple)],
            heading=_("Tags"),
        ),
    ]

    class Meta:
        abstract = True
