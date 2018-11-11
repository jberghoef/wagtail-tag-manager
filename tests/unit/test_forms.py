import pytest

from wagtail_tag_manager.forms import ConsentForm
from wagtail_tag_manager.strategy import TagStrategy


@pytest.mark.django_db
def test_consent_form():
    form = ConsentForm()

    assert "functional" in form.fields
    assert "analytical" in form.fields
    assert "traceable" in form.fields

    assert form.fields["functional"].required is True
    assert form.fields["functional"].disabled is True
    assert form.fields["functional"].initial is True

    assert form.fields["analytical"].required is False
    assert form.fields["analytical"].disabled is False
    assert form.fields["analytical"].initial is True

    assert form.fields["traceable"].required is False
    assert form.fields["traceable"].disabled is False
    assert form.fields["traceable"].initial is False


@pytest.mark.django_db
def test_consent_form_initial(rf, site):
    request = rf.get(site.root_page.url)
    request.COOKIES = {
        **request.COOKIES,
        "wtm_functional": "true",
        "wtm_analytical": "false",
        "wtm_traceable": "true",
    }

    cookie_state = TagStrategy(request).cookie_state
    form = ConsentForm(initial=cookie_state)

    assert "functional" in form.fields
    assert "analytical" in form.fields
    assert "traceable" in form.fields

    assert form.fields["functional"].initial is True
    assert form.fields["analytical"].initial is False
    assert form.fields["traceable"].initial is True
