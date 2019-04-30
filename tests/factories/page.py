import factory
from django.utils.text import slugify
from wagtail_factories.factories import PageFactory

from tests.site.pages.models import ContentPage, TaggableContentPage


class ContentPageFactory(PageFactory):
    title = "Test page"
    slug = factory.LazyAttribute(lambda obj: slugify(obj.title))

    class Meta:
        model = ContentPage


class TaggableContentPageFactory(ContentPageFactory):
    class Meta:
        model = TaggableContentPage
