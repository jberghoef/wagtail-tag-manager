import pytest

from tests.factories.tag import (
    tag_lazy_marketing,
    tag_lazy_necessary,
    tag_lazy_preferences,
    tag_instant_necessary,
)
from tests.factories.trigger import TriggerFactory, TriggerConditionFactory
from wagtail_tag_manager.models import (
    Tag,
    Trigger,
    Constant,
    Variable,
    TagTypeSettings,
    TriggerCondition,
    CookieDeclaration,
)


@pytest.mark.django_db
def test_tag_type_settings():
    config = TagTypeSettings().all()

    assert "necessary" in config
    assert "preferences" in config
    assert "statistics" in config
    assert "marketing" in config

    config = TagTypeSettings().include("required").result()

    assert "necessary" in config
    assert "preferences" not in config
    assert "statistics" not in config
    assert "marketing" not in config

    config = TagTypeSettings().include("initial").result()

    assert "necessary" not in config
    assert "preferences" in config
    assert "statistics" not in config
    assert "marketing" not in config

    config = TagTypeSettings().exclude("initial").result()

    assert "necessary" in config
    assert "preferences" not in config
    assert "statistics" in config
    assert "marketing" in config

    config = TagTypeSettings().exclude("required").exclude("initial").result()

    assert "necessary" not in config
    assert "preferences" not in config
    assert "statistics" in config
    assert "marketing" in config

    config = TagTypeSettings().exclude("").result()

    assert "necessary" in config
    assert "preferences" in config
    assert "statistics" in config
    assert "marketing" not in config


@pytest.mark.django_db
def test_tag_queries():
    tag_instant_necessary()
    tag_lazy_necessary()

    tags = Tag.objects.all()
    assert len(tags) == 2

    tags = Tag.objects.instant()
    assert len(tags) == 1

    tags = Tag.objects.lazy()
    assert len(tags) == 1


@pytest.mark.django_db
def test_tag_create():
    expected = '<script>\n console.log("necessary instant")\n</script>\n'

    tag = Tag.objects.create(
        name="necessary instant 1",
        content='<script>console.log("necessary instant")</script>',
    )
    assert tag.content == expected
    assert tag in Tag.objects.all()

    tag = Tag.objects.create(
        name="necessary instant 2", content='console.log("necessary instant")'
    )
    assert tag.content == expected
    assert tag in Tag.objects.all()

    expected = "<style>\n body { background-color: red; }\n</style>\n"

    tag = Tag.objects.create(
        name="necessary instant 3",
        content="<style>body { background-color: red; }</style>",
    )
    assert tag.content == expected
    assert tag in Tag.objects.all()


@pytest.mark.django_db
def test_constant_create():
    constant = Constant.objects.create(name="Constant", key="key", value="value")
    assert constant in Constant.objects.all()


@pytest.mark.django_db
def test_variable_create():
    variable = Variable.objects.create(
        name="Variable", key="key", variable_type="_cookie+"
    )
    assert variable in Variable.objects.all()


@pytest.mark.django_db
def test_variable_types(rf):
    request = rf.get("/wtm/")

    repath_variable = Variable.objects.create(
        name="RePath variable",
        key="repath_variable",
        variable_type="_repath+",
        value=r"(?:^\/)wtm(?:\/$)",
    )
    assert repath_variable.get_value(request) == "/wtm/"

    request.COOKIES = {"wtm_test": "hello, world"}
    cookie_variable = Variable.objects.create(
        name="Cookie variable",
        key="cookie_variable",
        variable_type="_cookie+",
        value="wtm_test",
    )
    assert cookie_variable.get_value(request) == "hello, world"


@pytest.mark.django_db
def test_trigger_create():
    trigger = Trigger.objects.create(name="Trigger")
    assert trigger in Trigger.objects.all()

    trigger_condition = TriggerConditionFactory(trigger=trigger)

    assert trigger_condition in trigger.conditions.all()

    tag_necessary = tag_lazy_necessary()
    tag_preferences = tag_lazy_preferences()
    tag_marketing = tag_lazy_marketing()

    trigger.tags.add(tag_necessary)
    trigger.tags.add(tag_preferences)
    trigger.tags.add(tag_marketing)

    assert tag_necessary in trigger.tags.all().sorted()
    assert tag_preferences in trigger.tags.all()
    assert tag_marketing in trigger.tags.all()


@pytest.mark.django_db
def test_trigger_condition_create():
    trigger = TriggerFactory()
    trigger_condition = TriggerCondition.objects.create(
        variable="navigation_path", value="/", trigger=trigger
    )

    assert trigger_condition in TriggerCondition.objects.all()


@pytest.mark.django_db
def test_cookie_declaration_create():
    cookie_declaration = CookieDeclaration.objects.create(
        cookie_type="necessary",
        name="Necessary cookie",
        domain="localhost",
        purpose="Lorem ipsum",
    )

    assert cookie_declaration in CookieDeclaration.objects.all()
