import factory

from wagtail_tag_manager import models


class VariableFactory(factory.DjangoModelFactory):
    name = 'Variable'
    key = 'key'
    variable_type = 'path'
    value = 'value'

    class Meta:
        model = models.Variable
