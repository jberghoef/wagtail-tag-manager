import factory

from wagtail_tag_manager import models


class TriggerFactory(factory.DjangoModelFactory):
    name = 'Trigger'
    pattern = '[?&]state=(?P<state>\S+)'

    class Meta:
        model = models.Trigger
