import pytest

from wagtail_tag_manager.forms import ConsentForm
from wagtail_tag_manager.utils import dict_to_base64
from wagtail_tag_manager.strategy import TagStrategy


@pytest.mark.django_db
def test_consent_form():
    form = ConsentForm()

    assert "necessary" in form.fields
    assert "preferences" in form.fields
    assert "marketing" in form.fields

    assert form.fields["necessary"].required is True
    assert form.fields["necessary"].disabled is True
    assert form.fields["necessary"].initial is True

    assert form.fields["preferences"].required is False
    assert form.fields["preferences"].disabled is False
    assert form.fields["preferences"].initial is True

    assert form.fields["marketing"].required is False
    assert form.fields["marketing"].disabled is False
    assert form.fields["marketing"].initial is False


@pytest.mark.django_db(transaction=True)
def test_consent_form_initial(rf, site):
    request = rf.get(site.root_page.url)
    request.COOKIES = {
        **request.COOKIES,
        "wtm": dict_to_base64(
            {
                "meta": {},
                "state": {
                    "necessary": "true",
                    "preferences": "false",
                    "marketing": "true",
                },
            }
        ),
    }

    cookie_state = TagStrategy(request).cookie_state
    form = ConsentForm(initial=cookie_state)

    assert "necessary" in form.fields
    assert "preferences" in form.fields
    assert "marketing" in form.fields

    assert form.fields["necessary"].initial is True
    assert form.fields["preferences"].initial is False
    assert form.fields["marketing"].initial is True
