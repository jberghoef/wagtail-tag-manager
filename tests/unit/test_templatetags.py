import pytest
from django.template import Template, RequestContext
from django.template.base import Token, Parser, TokenType
from django.template.context import make_context
from django.template.exceptions import TemplateDoesNotExist

from tests.factories.tag import (
    tag_instant_marketing,
    tag_instant_necessary,
    tag_instant_preferences,
)
from wagtail_tag_manager.utils import dict_to_base64
from wagtail_tag_manager.models import Tag, CookieDeclaration
from wagtail_tag_manager.templatetags.wtm_tags import (
    wtm_include,
    wtm_tag_table,
    wtm_cookie_bar,
    wtm_manage_form,
    wtm_instant_tags,
    wtm_lazy_manager,
    wtm_declaration_table,
)


@pytest.mark.django_db
def test_wtm_include_necessary(rf, site):
    expected_result = '<link href="/static/test.css" rel="stylesheet" type="text/css"/>'

    token = Token(
        token_type=TokenType.TEXT, contents='wtm_include "necessary" "test.css"'
    )
    parser = Parser(tokens=[token])
    node = wtm_include(parser, token)

    request = rf.get(site.root_page.url)
    result = node.render(context=make_context({"request": request}))

    assert result == expected_result

    request.COOKIES = {
        "wtm": dict_to_base64(
            {
                "meta": {},
                "state": {
                    "necessary": "false",
                },
            }
        )
    }
    result = node.render(context=make_context({"request": request}))

    assert result == expected_result

    request.COOKIES = {
        "wtm": dict_to_base64(
            {
                "meta": {},
                "state": {
                    "necessary": "true",
                },
            }
        )
    }
    result = node.render(context=make_context({"request": request}))

    assert result == expected_result


@pytest.mark.django_db
def test_wtm_include_preferences(rf, site):
    expected_result = '<script src="/static/test.js" type="text/javascript"></script>'

    token = Token(
        token_type=TokenType.TEXT, contents='wtm_include "preferences" "test.js"'
    )
    parser = Parser(tokens=[token])
    node = wtm_include(parser, token)

    request = rf.get(site.root_page.url)
    result = node.render(context=make_context({"request": request}))

    assert result == expected_result

    request.COOKIES = {
        "wtm": dict_to_base64(
            {
                "meta": {},
                "state": {
                    "preferences": "false",
                },
            }
        )
    }
    result = node.render(context=make_context({"request": request}))

    assert result == ""

    request.COOKIES = {
        "wtm": dict_to_base64(
            {
                "meta": {},
                "state": {
                    "preferences": "true",
                },
            }
        )
    }
    result = node.render(context=make_context({"request": request}))

    assert result == expected_result


@pytest.mark.django_db
def test_wtm_include_marketing(rf, site):
    token = Token(
        token_type=TokenType.TEXT, contents='wtm_include "marketing" "test.html"'
    )
    parser = Parser(tokens=[token])
    node = wtm_include(parser, token)

    with pytest.raises(TemplateDoesNotExist):
        request = rf.get(site.root_page.url)
        node.render(context=make_context({"request": request}))

        request.COOKIES = {
            "wtm": dict_to_base64(
                {
                    "meta": {},
                    "state": {
                        "marketing": "false",
                    },
                }
            )
        }
        node.render(context=make_context({"request": request}))

        request.COOKIES = {
            "wtm": dict_to_base64(
                {
                    "meta": {},
                    "state": {
                        "marketing": "true",
                    },
                }
            )
        }
        node.render(context=make_context({"request": request}))


@pytest.mark.django_db
def test_wtm_instant_tags(rf, site):
    tag_instant_necessary(tag_location=Tag.TOP_HEAD)
    tag_instant_preferences(tag_location=Tag.BOTTOM_HEAD)
    tag_instant_marketing(tag_location=Tag.TOP_BODY)

    request = rf.get(site.root_page.url)

    context = wtm_instant_tags({"request": request})
    assert "tags" in context
    assert len(context.get("tags")) == 1

    request.COOKIES = {
        "wtm": dict_to_base64(
            {
                "meta": {},
                "state": {
                    "necessary": "true",
                    "preferences": "true",
                },
            }
        )
    }
    context = wtm_instant_tags({"request": request})
    assert "tags" in context
    assert len(context.get("tags")) == 2

    request.COOKIES = {
        "wtm": dict_to_base64(
            {
                "meta": {},
                "state": {
                    "necessary": "true",
                    "preferences": "true",
                    "marketing": "true",
                },
            }
        )
    }
    context = wtm_instant_tags({"request": request})
    assert "tags" in context
    assert len(context.get("tags")) == 3

    context = wtm_instant_tags({"request": request}, location="top_head")
    assert "tags" in context
    assert len(context.get("tags")) == 1
    assert "necessary instant" in context.get("tags")[0]

    context = wtm_instant_tags({"request": request}, location="bottom_head")
    assert "tags" in context
    assert len(context.get("tags")) == 1
    assert "preferences instant" in context.get("tags")[0]

    context = wtm_instant_tags({"request": request}, location="top_body")
    assert "tags" in context
    assert len(context.get("tags")) == 1
    assert "marketing instant" in context.get("tags")[0]

    with pytest.raises(KeyError):
        wtm_instant_tags({"request": request}, location="middle_body")


@pytest.mark.django_db
def test_wtm_lazy_manager():
    context = wtm_lazy_manager()

    assert "config" in context
    assert "config_url" in context.get("config")
    assert "lazy_url" in context.get("config")


@pytest.mark.django_db
def test_wtm_cookie_bar(rf, site):
    request = rf.get(site.root_page.url)
    context = wtm_cookie_bar(context={"request": request})

    assert "manage_view" in context
    assert context.get("manage_view") is True


@pytest.mark.django_db
def test_wtm_manage_form(rf, site):
    request = rf.get(site.root_page.url)
    context = wtm_manage_form(context={"request": request})
    # The tag hands the template a bound ConsentForm for every tag type.
    assert "form" in context
    assert set(context["form"].fields) == {
        "necessary",
        "preferences",
        "statistics",
        "marketing",
    }


@pytest.mark.django_db
def test_wtm_manage_form_without_request_renders_nothing():
    assert wtm_manage_form(context={}) == ""


@pytest.mark.django_db
def test_wtm_tag_table_lists_all_tags():
    tag = tag_instant_necessary()
    context = wtm_tag_table(context={})
    assert tag in list(context["tags"])


@pytest.mark.django_db
def test_wtm_declaration_table_lists_declarations():
    declaration = CookieDeclaration.objects.create(
        cookie_type="necessary",
        name="Necessary cookie",
        domain="localhost",
        purpose="Lorem ipsum",
    )
    context = wtm_declaration_table(context={})
    assert declaration in list(context["declarations"])


@pytest.mark.django_db
def test_wtm_include_inline_block_renders_when_consented(rf, site):
    # The block form (no src) renders its body only when consent allows it.
    request = rf.get(site.root_page.url)
    tpl = Template(
        '{% load wtm_tags %}'
        '{% wtm_include "necessary" %}<p>SECRET</p>{% wtm_endinclude %}'
    )
    # necessary is `required` -> always included -> body renders.
    assert "<p>SECRET</p>" in tpl.render(RequestContext(request, {}))


@pytest.mark.django_db
def test_wtm_include_inline_block_hidden_without_consent(rf, site):
    request = rf.get(site.root_page.url)
    request.COOKIES = {
        "wtm": dict_to_base64({"meta": {}, "state": {"marketing": "unset"}})
    }
    tpl = Template(
        '{% load wtm_tags %}'
        '{% wtm_include "marketing" %}<p>SECRET</p>{% wtm_endinclude %}'
    )
    # marketing is default -> withheld while unset -> body suppressed.
    assert "<p>SECRET</p>" not in tpl.render(RequestContext(request, {}))
