import factory

from wagtail_tag_manager import models


class VariableFactory(factory.django.DjangoModelFactory):
    name = "Variable"
    key = "key"
    variable_type = "_cookie+"
    value = "wtm"

    class Meta:
        model = models.Variable
