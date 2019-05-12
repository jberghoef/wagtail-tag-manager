import pytest

from tests.factories.trigger import TriggerFactory
from wagtail_tag_manager.models import TriggerCondition


@pytest.mark.django_db
def test_trigger_condition_empty():
    trigger = TriggerFactory()
    trigger_condition = TriggerCondition.objects.create(
        variable="trigger_value", value="test", trigger=trigger
    )

    assert trigger_condition.validate({}) is False


@pytest.mark.django_db
def test_trigger_condition_exact_match():
    trigger = TriggerFactory()
    trigger_condition = TriggerCondition.objects.create(
        condition_type=TriggerCondition.CONDITION_EXACT_MATCH,
        variable="trigger_value",
        value="test",
        trigger=trigger,
    )

    assert trigger_condition.validate({"trigger_value": "tes"}) is False

    assert trigger_condition.validate({"trigger_value": "test"}) is True


@pytest.mark.django_db
def test_trigger_condition_not_exact_match():
    trigger = TriggerFactory()
    trigger_condition = TriggerCondition.objects.create(
        condition_type=TriggerCondition.CONDITION_NOT_EXACT_MATCH,
        variable="trigger_value",
        value="test",
        trigger=trigger,
    )

    assert trigger_condition.validate({"trigger_value": "test"}) is False

    assert trigger_condition.validate({"trigger_value": "tes"}) is True


@pytest.mark.django_db
def test_trigger_condition_contains():
    trigger = TriggerFactory()
    trigger_condition = TriggerCondition.objects.create(
        condition_type=TriggerCondition.CONDITION_CONTAINS,
        variable="trigger_value",
        value="test",
        trigger=trigger,
    )

    assert trigger_condition.validate({"trigger_value": "tesing"}) is False

    assert trigger_condition.validate({"trigger_value": "testing"}) is True


@pytest.mark.django_db
def test_trigger_condition_not_contains():
    trigger = TriggerFactory()
    trigger_condition = TriggerCondition.objects.create(
        condition_type=TriggerCondition.CONDITION_NOT_CONTAINS,
        variable="trigger_value",
        value="test",
        trigger=trigger,
    )

    assert trigger_condition.validate({"trigger_value": "testing"}) is False

    assert trigger_condition.validate({"trigger_value": "tesing"}) is True


@pytest.mark.django_db
def test_trigger_condition_starts_with():
    trigger = TriggerFactory()
    trigger_condition = TriggerCondition.objects.create(
        condition_type=TriggerCondition.CONDITION_STARTS_WITH,
        variable="trigger_value",
        value="test",
        trigger=trigger,
    )

    assert trigger_condition.validate({"trigger_value": "esting"}) is False

    assert trigger_condition.validate({"trigger_value": "testing"}) is True


@pytest.mark.django_db
def test_trigger_condition_not_starts_with():
    trigger = TriggerFactory()
    trigger_condition = TriggerCondition.objects.create(
        condition_type=TriggerCondition.CONDITION_NOT_STARTS_WITH,
        variable="trigger_value",
        value="test",
        trigger=trigger,
    )

    assert trigger_condition.validate({"trigger_value": "testing"}) is False

    assert trigger_condition.validate({"trigger_value": "esting"}) is True


@pytest.mark.django_db
def test_trigger_condition_ends_with():
    trigger = TriggerFactory()
    trigger_condition = TriggerCondition.objects.create(
        condition_type=TriggerCondition.CONDITION_ENDS_WITH,
        variable="trigger_value",
        value="test",
        trigger=trigger,
    )

    assert trigger_condition.validate({"trigger_value": "testing"}) is False

    assert trigger_condition.validate({"trigger_value": "test"}) is True


@pytest.mark.django_db
def test_trigger_condition_not_ends_with():
    trigger = TriggerFactory()
    trigger_condition = TriggerCondition.objects.create(
        condition_type=TriggerCondition.CONDITION_NOT_ENDS_WITH,
        variable="trigger_value",
        value="test",
        trigger=trigger,
    )

    assert trigger_condition.validate({"trigger_value": "test"}) is False

    assert trigger_condition.validate({"trigger_value": "testing"}) is True


@pytest.mark.django_db
def test_trigger_condition_regex_match():
    trigger = TriggerFactory()
    trigger_condition = TriggerCondition.objects.create(
        condition_type=TriggerCondition.CONDITION_REGEX_MATCH,
        variable="trigger_value",
        value=r"^[a-z]+$",
        trigger=trigger,
    )

    assert trigger_condition.validate({"trigger_value": "test1"}) is False

    assert trigger_condition.validate({"trigger_value": "test"}) is True


@pytest.mark.django_db
def test_trigger_condition_not_regex_match():
    trigger = TriggerFactory()
    trigger_condition = TriggerCondition.objects.create(
        condition_type=TriggerCondition.CONDITION_NOT_REGEX_MATCH,
        variable="trigger_value",
        value=r"^[a-z]+$",
        trigger=trigger,
    )

    assert trigger_condition.validate({"trigger_value": "test"}) is False

    assert trigger_condition.validate({"trigger_value": "test1"}) is True


@pytest.mark.django_db
def test_trigger_condition_regex_imatch():
    trigger = TriggerFactory()
    trigger_condition = TriggerCondition.objects.create(
        condition_type=TriggerCondition.CONDITION_REGEX_IMATCH,
        variable="trigger_value",
        value=r"^[a-z]+$",
        trigger=trigger,
    )

    assert trigger_condition.validate({"trigger_value": "TEST1"}) is False

    assert trigger_condition.validate({"trigger_value": "TEST"}) is True


@pytest.mark.django_db
def test_trigger_condition_not_regex_imatch():
    trigger = TriggerFactory()
    trigger_condition = TriggerCondition.objects.create(
        condition_type=TriggerCondition.CONDITION_NOT_REGEX_IMATCH,
        variable="trigger_value",
        value=r"^[a-z]+$",
        trigger=trigger,
    )

    assert trigger_condition.validate({"trigger_value": "TEST"}) is False

    assert trigger_condition.validate({"trigger_value": "TEST1"}) is True


@pytest.mark.django_db
def test_trigger_condition_lower_than():
    trigger = TriggerFactory()
    trigger_condition = TriggerCondition.objects.create(
        condition_type=TriggerCondition.CONDITION_LT,
        variable="trigger_value",
        value="1",
        trigger=trigger,
    )

    assert trigger_condition.validate({"trigger_value": "1.1"}) is False

    assert trigger_condition.validate({"trigger_value": "1"}) is False

    assert trigger_condition.validate({"trigger_value": "0.9"}) is True


@pytest.mark.django_db
def test_trigger_condition_lower_than_equal():
    trigger = TriggerFactory()
    trigger_condition = TriggerCondition.objects.create(
        condition_type=TriggerCondition.CONDITION_LTE,
        variable="trigger_value",
        value="1",
        trigger=trigger,
    )

    assert trigger_condition.validate({"trigger_value": "1.1"}) is False

    assert trigger_condition.validate({"trigger_value": "1"}) is True

    assert trigger_condition.validate({"trigger_value": "0.9"}) is True


@pytest.mark.django_db
def test_trigger_condition_greater_than():
    trigger = TriggerFactory()
    trigger_condition = TriggerCondition.objects.create(
        condition_type=TriggerCondition.CONDITION_GT,
        variable="trigger_value",
        value="1",
        trigger=trigger,
    )

    assert trigger_condition.validate({"trigger_value": "1.1"}) is True

    assert trigger_condition.validate({"trigger_value": "1"}) is False

    assert trigger_condition.validate({"trigger_value": "0.9"}) is False


@pytest.mark.django_db
def test_trigger_condition_greater_than_equal():
    trigger = TriggerFactory()
    trigger_condition = TriggerCondition.objects.create(
        condition_type=TriggerCondition.CONDITION_GTE,
        variable="trigger_value",
        value="1",
        trigger=trigger,
    )

    assert trigger_condition.validate({"trigger_value": "1.1"}) is True

    assert trigger_condition.validate({"trigger_value": "1"}) is True

    assert trigger_condition.validate({"trigger_value": "0.9"}) is False
