import factory
from wagtail.models import Locale


class LocaleFactory(factory.django.DjangoModelFactory):
    language_code = "en"

    class Meta:
        model = Locale
