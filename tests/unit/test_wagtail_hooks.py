import pytest

from tests.factories.tag import TagFactory
from tests.factories.trigger import TriggerFactory
from tests.factories.constant import ConstantFactory
from tests.factories.variable import VariableFactory
from wagtail_tag_manager.wagtail_hooks import (
    TagModelAdmin, TriggerModelAdmin, ConstantModelAdmin, VariableModelAdmin)


@pytest.mark.django_db
def test_name_display():
    constant = ConstantFactory(description="Test")
    constant_model_admin = ConstantModelAdmin()

    description = constant_model_admin.name_display(constant)
    assert constant.description in description

    variable = VariableFactory(key="var", description="Test")
    variable_model_admin = VariableModelAdmin()

    description = variable_model_admin.name_display(variable)
    assert variable.description in description

    tag = TagFactory(description="Test")
    tag_model_admin = TagModelAdmin()

    description = tag_model_admin.name_display(tag)
    assert tag.description in description

    trigger = TriggerFactory(description="Test")
    trigger_model_admin = TriggerModelAdmin()

    description = trigger_model_admin.name_display(trigger)
    assert tag.description in description


@pytest.mark.django_db
def test_no_description_display():
    constant = ConstantFactory()
    constant_model_admin = ConstantModelAdmin()

    description = constant_model_admin.name_display(constant)
    assert constant.name == description

    variable = VariableFactory(key="var")
    variable_model_admin = VariableModelAdmin()

    description = variable_model_admin.name_display(variable)
    assert variable.name == description

    tag = TagFactory()
    tag_model_admin = TagModelAdmin()

    description = tag_model_admin.name_display(tag)
    assert tag.name == description

    trigger = TriggerFactory()
    trigger_model_admin = TriggerModelAdmin()

    description = trigger_model_admin.name_display(trigger)
    assert trigger.name == description


@pytest.mark.django_db
def test_tag_count():
    tag1 = TagFactory(name="tag1")
    tag2 = TagFactory(name="tag2")

    trigger = TriggerFactory()
    trigger.tags.add(tag1, tag2)
    trigger_model_admin = TriggerModelAdmin()

    result = trigger_model_admin.tags_count(trigger)
    assert result == "2 tag(s)"
