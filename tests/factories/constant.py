import factory

from wagtail_tag_manager import models


class ConstantFactory(factory.django.DjangoModelFactory):
    name = "Constant"
    key = "key"
    value = "value"

    class Meta:
        model = models.Constant
