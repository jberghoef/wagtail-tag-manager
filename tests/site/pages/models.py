from django.db import models
from wagtail.fields import RichTextField
from wagtail.models import Page
from wagtail.admin.panels import FieldPanel

from wagtail_tag_manager.mixins import TagMixin


class ContentPage(Page):
    subtitle = models.CharField(max_length=255, blank=True, default="")
    body = RichTextField(blank=True, default="")

    content_panels = Page.content_panels + [FieldPanel("subtitle"), FieldPanel("body")]


class TaggableContentPage(TagMixin, ContentPage):
    pass
