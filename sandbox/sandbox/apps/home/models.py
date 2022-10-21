from wagtail.admin.edit_handlers import FieldPanel
from wagtail.core.fields import RichTextField
from wagtail.core.models import Page

from wagtail_tag_manager.decorators import register_variable
from wagtail_tag_manager.mixins import TagMixin
from wagtail_tag_manager.options import CustomVariable


class HomePage(TagMixin, Page):
    content = RichTextField()

    content_panels = Page.content_panels + [
        FieldPanel('content'),
    ]


@register_variable
class Variable(CustomVariable):
    name = "Custom variable"
    description = "Returns a custom value."
    key = "custom"

    def get_value(self, request):
        return "This is a custom variable."
