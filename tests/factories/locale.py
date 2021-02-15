import factory
from wagtail.core.models import Locale


class LocaleFactory(factory.django.DjangoModelFactory):
    language_code = "en"

    class Meta:
        model = Locale
