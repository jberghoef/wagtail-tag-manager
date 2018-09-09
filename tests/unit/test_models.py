import pytest

from tests.factories.tag import (
    tag_lazy_traceable,
    tag_lazy_analytical,
    tag_lazy_functional,
    tag_instant_functional,
)
from tests.factories.trigger import TriggerFactory
from wagtail_tag_manager.models import Tag, Trigger, Constant, Variable, TagTypeSettings


@pytest.mark.django_db
def test_tag_type_settings():
    config = TagTypeSettings().all()

    assert "functional" in config
    assert "analytical" in config
    assert "traceable" in config

    config = TagTypeSettings().include("required").result()

    assert "functional" in config
    assert "analytical" not in config
    assert "traceable" not in config

    config = TagTypeSettings().include("initial").result()

    assert "functional" not in config
    assert "analytical" in config
    assert "traceable" not in config

    config = TagTypeSettings().exclude("initial").result()

    assert "functional" in config
    assert "analytical" not in config
    assert "traceable" in config

    config = TagTypeSettings().exclude("required").exclude("initial").result()

    assert "functional" not in config
    assert "analytical" not in config
    assert "traceable" in config

    config = TagTypeSettings().exclude("").result()

    assert "functional" in config
    assert "analytical" in config
    assert "traceable" not in config


@pytest.mark.django_db
def test_tag_queries():
    tag_instant_functional()
    tag_lazy_functional()

    tags = Tag.objects.all()
    assert len(tags) == 2

    tags = Tag.objects.instant()
    assert len(tags) == 1

    tags = Tag.objects.lazy()
    assert len(tags) == 1


@pytest.mark.django_db
def test_tag_create():
    expected = '<script>\n console.log("functional instant")\n</script>'

    tag = Tag.objects.create(
        name="functional instant 1",
        content='<script>console.log("functional instant")</script>',
    )
    assert tag.content == expected
    assert tag in Tag.objects.all()

    tag = Tag.objects.create(
        name="functional instant 2", content='console.log("functional instant")'
    )
    assert tag.content == expected
    assert tag in Tag.objects.all()


@pytest.mark.django_db
def test_constant_create():
    constant = Constant.objects.create(name="Constant", key="key", value="value")
    assert constant in Constant.objects.all()


@pytest.mark.django_db
def test_variable_create():
    variable = Variable.objects.create(name="Variable", key="key", variable_type="path")
    assert variable in Variable.objects.all()


@pytest.mark.django_db
def test_trigger_create():
    trigger = Trigger.objects.create(name="Trigger", pattern="[?&]state=(?P<state>\S+)")
    assert trigger in Trigger.objects.all()

    tag_functional = tag_lazy_functional()
    tag_analytical = tag_lazy_analytical()
    tag_traceable = tag_lazy_traceable()

    trigger.tags.add(tag_functional)
    trigger.tags.add(tag_analytical)
    trigger.tags.add(tag_traceable)

    assert tag_functional in trigger.tags.all()
    assert tag_analytical in trigger.tags.all()
    assert tag_traceable in trigger.tags.all()
