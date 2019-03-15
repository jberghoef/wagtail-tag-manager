import pytest

from wagtail_tag_manager.context_processors import cookie_state


@pytest.mark.django_db
def test_cookie_state(rf, site):
    request = rf.get(site.root_page.url)
    assert cookie_state(request) == {
        "wtm_cookie_state": {
            "analytical": True,
            "continue": True,
            "functional": True,
            "traceable": False,
        }
    }
