import pytest
from django.template.base import Token, Parser, TokenType
from django.template.context import make_context
from django.template.exceptions import TemplateDoesNotExist

from tests.factories.tag import (
    tag_instant_traceable,
    tag_instant_analytical,
    tag_instant_functional,
)
from wagtail_tag_manager.models import Tag
from wagtail_tag_manager.templatetags.wtm_tags import (
    wtm_include,
    wtm_cookie_bar,
    wtm_instant_tags,
    wtm_lazy_manager,
)


@pytest.mark.django_db
def test_wtm_include_functional(rf, site):
    expected_result = '<link href="/static/test.css" rel="stylesheet" type="text/css"/>'

    token = Token(
        token_type=TokenType.TEXT, contents='wtm_include "functional" "test.css"'
    )
    parser = Parser(tokens=[token])
    node = wtm_include(parser, token)

    request = rf.get(site.root_page.url)
    result = node.render(context=make_context({"request": request}))

    assert result == expected_result

    request.COOKIES = {"wtm": "functional:false"}
    result = node.render(context=make_context({"request": request}))

    assert result == expected_result

    request.COOKIES = {"wtm": "functional:true"}
    result = node.render(context=make_context({"request": request}))

    assert result == expected_result


@pytest.mark.django_db
def test_wtm_include_analytical(rf, site):
    expected_result = '<script src="/static/test.js" type="text/javascript"></script>'

    token = Token(
        token_type=TokenType.TEXT, contents='wtm_include "analytical" "test.js"'
    )
    parser = Parser(tokens=[token])
    node = wtm_include(parser, token)

    request = rf.get(site.root_page.url)
    result = node.render(context=make_context({"request": request}))

    assert result == expected_result

    request.COOKIES = {"wtm": "analytical:false"}
    result = node.render(context=make_context({"request": request}))

    assert result == ""

    request.COOKIES = {"wtm": "analytical:true"}
    result = node.render(context=make_context({"request": request}))

    assert result == expected_result


@pytest.mark.django_db
def test_wtm_include_traceable(rf, site):
    token = Token(
        token_type=TokenType.TEXT, contents='wtm_include "traceable" "test.html"'
    )
    parser = Parser(tokens=[token])
    node = wtm_include(parser, token)

    with pytest.raises(TemplateDoesNotExist):
        request = rf.get(site.root_page.url)
        node.render(context=make_context({"request": request}))

        request.COOKIES = {"wtm": "traceable:false"}
        node.render(context=make_context({"request": request}))

        request.COOKIES = {"wtm": "traceable:true"}
        node.render(context=make_context({"request": request}))


@pytest.mark.django_db
def test_wtm_instant_tags(rf, site):
    tag_instant_functional(tag_location=Tag.TOP_HEAD)
    tag_instant_analytical(tag_location=Tag.BOTTOM_HEAD)
    tag_instant_traceable(tag_location=Tag.TOP_BODY)

    request = rf.get(site.root_page.url)

    context = wtm_instant_tags({"request": request})
    assert "tags" in context
    assert len(context.get("tags")) == 1

    request.COOKIES = {"wtm": "functional:true|analytical:true"}
    context = wtm_instant_tags({"request": request})
    assert "tags" in context
    assert len(context.get("tags")) == 2

    request.COOKIES = {"wtm": "functional:true|analytical:true|traceable:true"}
    context = wtm_instant_tags({"request": request})
    assert "tags" in context
    assert len(context.get("tags")) == 3

    context = wtm_instant_tags({"request": request}, location="top_head")
    assert "tags" in context
    assert len(context.get("tags")) == 1
    assert "functional instant" in context.get("tags")[0]

    context = wtm_instant_tags({"request": request}, location="bottom_head")
    assert "tags" in context
    assert len(context.get("tags")) == 1
    assert "analytical instant" in context.get("tags")[0]

    context = wtm_instant_tags({"request": request}, location="top_body")
    assert "tags" in context
    assert len(context.get("tags")) == 1
    assert "traceable instant" in context.get("tags")[0]

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
