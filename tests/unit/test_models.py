import pytest
from django.core.exceptions import ValidationError

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
def test_variable_get_value_attribute_branches(rf):
    request = rf.get("/some/path/")
    # Plain request attribute (no "_" prefix, no "."): getattr(request, type).
    plain = Variable(name="p", key="p", variable_type="path")
    assert plain.get_value(request) == "/some/path/"
    # Dotted path resolves via attrgetter against the request.
    request.obj = type("O", (), {"inner": "deep"})()
    dotted = Variable(name="d", key="d", variable_type="obj.inner")
    assert dotted.get_value(request) == "deep"


@pytest.mark.django_db
def test_variable_repath_without_match_returns_empty(rf):
    request = rf.get("/foo/")
    variable = Variable(
        name="r", key="r", variable_type="_repath+", value="zzz-no-match"
    )
    assert variable.get_value(request) == ""


@pytest.mark.django_db
def test_variable_cookie_without_request_returns_empty():
    variable = Variable(name="c", key="c", variable_type="_cookie+", value="x")
    assert variable.get_value(None) == ""


@pytest.mark.django_db
def test_variable_create_context_renders_builtin_variables(rf, site):
    # create_context merges the built-in CustomVariables (config.py) with DB
    # variables and evaluates each. Assert the stable ones resolve correctly.
    request = rf.get("/wtm/?q=1")
    context = Variable.create_context(request)

    assert context["navigation_path"] == "/wtm/"
    assert context["navigation_full_path"] == "/wtm/?q=1"
    assert context["navigation_referrer"] == ""  # no HTTP_REFERER on the request
    assert "/wtm/" in context["navigation_url"]
    assert context["consent_marketing"] == "unset"  # no consent cookie yet
    assert context["wagtail_site"] == site.pk
    assert isinstance(context["rand"], int)


def test_builtin_variables_fall_back_when_request_lacks_attributes():
    # Each navigation/user CustomVariable defers to super().get_value() -> "" when
    # the request lacks the attribute it reads (e.g. a non-request object).
    from wagtail_tag_manager.decorators import get_variables

    variables = {variable.key: variable for variable in get_variables()}
    bare = object()  # no META / get_host / build_absolute_uri / user / session

    for key in (
        "navigation_referrer",
        "navigation_host",
        "navigation_url",
        "navigation_full_path",
        "user_id",
        "user_session",
    ):
        assert variables[key].get_value(bare) == ""


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
def test_trigger_get_value_casts_numbered_types_to_int():
    # Scroll/timer trigger types carry a numeric value and must surface as int
    # (JS consumes it as a number); other types stay as-is. as_dict strips "+".
    numbered = Trigger(name="n", trigger_type=Trigger.TYPE_TIMER_TIMEOUT, value="5")
    assert numbered.get_value() == 5
    assert numbered.as_dict()["type"] == "timer_timeout"

    plain = Trigger(name="p", trigger_type=Trigger.TYPE_FORM_SUBMIT, value="")
    assert plain.get_value() == ""


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


# --- Validation guardrails --------------------------------------------------
# These raise ValidationError so a broken tag/trigger/key-collision can never be
# saved. Intended behaviour derived from each model's clean() contract.


@pytest.mark.django_db
def test_tag_rejects_invalid_template():
    # An unclosed template tag must be refused, not stored and rendered later.
    with pytest.raises(ValidationError):
        Tag.objects.create(name="broken", content="{% if %}")


@pytest.mark.django_db
def test_trigger_requires_value_for_plus_type():
    # A "+"-suffixed trigger_type carries a value; omitting it is invalid.
    trigger = Trigger(name="t", trigger_type=Trigger.TYPE_TIMER_TIMEOUT, value="")
    with pytest.raises(ValidationError, match="value is required"):
        trigger.full_clean()


@pytest.mark.django_db
def test_trigger_rejects_value_for_non_plus_type():
    # A non-"+" trigger_type takes no value; supplying one is invalid.
    trigger = Trigger(name="t", trigger_type=Trigger.TYPE_FORM_SUBMIT, value="5")
    with pytest.raises(ValidationError, match="value is not allowed"):
        trigger.full_clean()


@pytest.mark.django_db
def test_variable_key_collides_with_constant():
    Constant.objects.create(name="C", key="dup", value="v")
    with pytest.raises(ValidationError):
        Variable.objects.create(name="V", key="dup", variable_type="_cookie+")


@pytest.mark.django_db
def test_constant_key_collides_with_variable():
    Variable.objects.create(name="V", key="dup2", variable_type="_cookie+")
    with pytest.raises(ValidationError):
        Constant.objects.create(name="C", key="dup2", value="v")
