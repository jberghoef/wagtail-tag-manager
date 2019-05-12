import pytest

from wagtail_tag_manager.widgets import VariableSelect
from wagtail_tag_manager.decorators import get_variables


@pytest.mark.django_db
def test_widget():
    vs = VariableSelect()
    assert len(vs.choices) == len(get_variables())
