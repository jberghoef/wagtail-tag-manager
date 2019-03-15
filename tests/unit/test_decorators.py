import pytest

from wagtail_tag_manager.decorators import register_variable, get_variables
from wagtail_tag_manager.options import CustomVariable


@pytest.mark.django_db
def test_register_variable():
    @register_variable
    class Variable(CustomVariable):
        name = "Custom variable"
        description = "Returns a custom value."
        key = "custom"

        def get_value(self, request):
            return "This is a custom variable."

    variables = get_variables()
    assert len(variables) == 1
