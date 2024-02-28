import pytest

from tests.factories.tag import (
    TagFactory,
    tag_lazy_marketing,
    tag_lazy_necessary,
    tag_lazy_preferences,
    tag_instant_marketing,
    tag_instant_necessary,
    tag_instant_preferences,
)
from tests.factories.trigger import TriggerFactory, TriggerConditionFactory
from tests.factories.constant import ConstantFactory
from tests.factories.variable import VariableFactory
from wagtail_tag_manager.models import (
    Tag,
    Trigger,
    Constant,
    Variable,
    TriggerCondition,
)


def get_expected_content(string):
    return '<script>\n console.log("{}")\n</script>\n'.format(string)


@pytest.mark.django_db
def test_tag_create():
    produced_tag = TagFactory()
    tag = Tag(
        name="necessary instant",
        content='<script>console.log("necessary instant")</script>',
    )

    assert produced_tag.name == tag.name
    assert produced_tag.tag_type == tag.tag_type
    assert produced_tag.content == get_expected_content(tag.name)


@pytest.mark.django_db
def test_tag_instant_necessary():
    produced_tag = tag_instant_necessary()
    tag = Tag(
        name="necessary instant",
        content='<script>console.log("necessary instant")</script>',
    )

    assert produced_tag.name == tag.name
    assert produced_tag.tag_type == tag.tag_type
    assert produced_tag.content == get_expected_content(tag.name)


@pytest.mark.django_db
def test_tag_instant_preferences():
    produced_tag = tag_instant_preferences()
    tag = Tag(
        name="preferences instant",
        tag_type="preferences",
        content='<script>console.log("preferences instant")</script>',
    )

    assert produced_tag.name == tag.name
    assert produced_tag.tag_type == tag.tag_type
    assert produced_tag.content == get_expected_content(tag.name)


@pytest.mark.django_db
def test_tag_instant_marketing():
    produced_tag = tag_instant_marketing()
    tag = Tag(
        name="marketing instant",
        tag_type="marketing",
        content='<script>console.log("marketing instant")</script>',
    )

    assert produced_tag.name == tag.name
    assert produced_tag.tag_type == tag.tag_type
    assert produced_tag.content == get_expected_content(tag.name)


@pytest.mark.django_db
def test_tag_lazy_necessary():
    produced_tag = tag_lazy_necessary()
    tag = Tag(
        name="necessary lazy", content='<script>console.log("necessary lazy")</script>'
    )

    assert produced_tag.name == tag.name
    assert produced_tag.tag_type == tag.tag_type
    assert produced_tag.content == get_expected_content(tag.name)


@pytest.mark.django_db
def test_tag_lazy_preferences():
    produced_tag = tag_lazy_preferences()
    tag = Tag(
        name="preferences lazy",
        tag_type="preferences",
        content='<script>console.log("preferences lazy")</script>',
    )

    assert produced_tag.name == tag.name
    assert produced_tag.tag_type == tag.tag_type
    assert produced_tag.content == get_expected_content(tag.name)


@pytest.mark.django_db
def test_tag_lazy_marketing():
    produced_tag = tag_lazy_marketing()
    tag = Tag(
        name="marketing lazy",
        tag_type="marketing",
        content='<script>console.log("marketing lazy")</script>',
    )

    assert produced_tag.name == tag.name
    assert produced_tag.tag_type == tag.tag_type
    assert produced_tag.content == get_expected_content(tag.name)


@pytest.mark.django_db
def test_constant_create():
    produced_constant = ConstantFactory()
    constant = Constant(name="Constant", key="key", value="value")

    assert produced_constant.name == constant.name
    assert produced_constant.key == constant.key
    assert produced_constant.value == constant.value


@pytest.mark.django_db
def test_variable_create():
    produced_variable = VariableFactory()
    variable = Variable(
        name="Variable", key="key", variable_type="_cookie+", value="wtm"
    )

    assert produced_variable.name == variable.name
    assert produced_variable.key == variable.key
    assert produced_variable.variable_type == variable.variable_type
    assert produced_variable.value == variable.value


@pytest.mark.django_db
def test_trigger_create():
    produced_trigger = TriggerFactory()
    trigger = Trigger(name="Trigger")

    assert produced_trigger.name == trigger.name


@pytest.mark.django_db
def test_trigger_condition_create():
    produced_trigger = TriggerFactory()
    produced_trigger_condition = TriggerConditionFactory(trigger=produced_trigger)
    trigger = Trigger(name="Trigger")
    trigger_condition = TriggerCondition(
        variable="navigation_path", value="/", trigger=trigger
    )

    assert produced_trigger.name == trigger.name
    assert produced_trigger_condition.value == trigger_condition.value
