import factory

from wagtail_tag_manager import models


class TriggerFactory(factory.DjangoModelFactory):
    name = "Trigger"
    slug = "trigger"

    class Meta:
        model = models.Trigger


class TriggerConditionFactory(factory.DjangoModelFactory):
    variable = "navigation_path"
    value = "/"

    class Meta:
        model = models.TriggerCondition
