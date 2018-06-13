from wagtail.admin.edit_handlers import RichTextFieldPanel
from wagtail.core.fields import RichTextField
from wagtail.core.models import Page


class HomePage(Page):
    content = RichTextField()

    content_panels = Page.content_panels + [
        RichTextFieldPanel('content'),
    ]
