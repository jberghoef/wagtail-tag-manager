import factory

from wagtail_tag_manager import models


class TriggerFactory(factory.django.DjangoModelFactory):
    name = "Trigger"
    slug = "trigger"

    class Meta:
        model = models.Trigger


class TriggerConditionFactory(factory.django.DjangoModelFactory):
    variable = "navigation_path"
    value = "/"

    class Meta:
        model = models.TriggerCondition
