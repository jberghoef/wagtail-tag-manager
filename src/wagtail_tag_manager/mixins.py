from django.db import models
from modelcluster.fields import ParentalManyToManyField
from modelcluster.models import ClusterableModel
from django.utils.translation import ugettext_lazy as _
from wagtail.admin.edit_handlers import FieldPanel, MultiFieldPanel, PublishingPanel

from wagtail_tag_manager.models import Tag
from wagtail_tag_manager.widgets import (
    HorizontalCheckboxSelectMultiple as CheckboxSelectMultiple,
)


class TagMixin(ClusterableModel):
    wtm_tags = ParentalManyToManyField(
        Tag,
        blank=True,
        related_name="pages",
        verbose_name=_("Tags"),
        help_text=_("The tags to include when this page is loaded."),
    )
    wtm_include_children = models.BooleanField(
        default=False,
        verbose_name=_("Include children"),
        help_text=_("Also include these tags on all children of this page."),
    )

    settings_panels = [
        PublishingPanel(),
        MultiFieldPanel(
            [
                FieldPanel("wtm_tags", widget=CheckboxSelectMultiple),
                FieldPanel("wtm_include_children"),
            ],
            heading=_("Tags"),
        ),
    ]

    class Meta:
        abstract = True
