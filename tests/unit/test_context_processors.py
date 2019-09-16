import pytest

from wagtail_tag_manager.context_processors import consent_state


@pytest.mark.django_db
def test_consent_state(rf, site):
    request = rf.get(site.root_page.url)
    assert consent_state(request) == {
        "wtm_consent_state": {
            "preferences": True,
            "statistics": True,
            "necessary": True,
            "marketing": False,
        }
    }
