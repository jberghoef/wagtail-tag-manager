import pytest

from wagtail_tag_manager.options import CustomVariable
from wagtail_tag_manager.decorators import get_variables, register_variable

BUILT_IN_COUNT = len(get_variables())


@pytest.mark.django_db
def test_default_variables():
    variables = get_variables()
    assert len(variables) == BUILT_IN_COUNT


@pytest.mark.django_db
def test_register_variable():
    @register_variable
    class Variable(CustomVariable):
        name = "Custom variable"
        description = "Returns a custom value."
        key = "custom1"

        def get_value(self, request):
            return "This is a custom variable."

    variables = get_variables()
    assert len(variables) == BUILT_IN_COUNT + 1


@pytest.mark.django_db
def test_register_variable_after():
    class Variable(CustomVariable):
        name = "Custom variable"
        description = "Returns a custom value."
        key = "custom2"

        def get_value(self, request):
            return "This is a custom variable."

    register_variable(Variable)

    variables = get_variables()
    assert len(variables) == BUILT_IN_COUNT + 2


@pytest.mark.django_db
def test_register_variable_invalid():
    class Variable(CustomVariable):
        name = "Custom variable"
        key = "custom3"

        def get_value(self, request):
            return "This is a custom variable."

    with pytest.raises(Exception):
        Variable()


@pytest.mark.django_db
def test_register_variable_subclass():
    class Variable(object):
        name = "Custom variable"
        description = "Returns a custom value."
        key = "custom4"

        def get_value(self, request):
            return "This is a custom variable."

    with pytest.raises(Exception):
        register_variable(Variable)

    variables = get_variables()
    assert len(variables) == BUILT_IN_COUNT + 2
