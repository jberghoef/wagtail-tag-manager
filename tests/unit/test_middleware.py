from http.cookies import SimpleCookie

import pytest

from tests.factories.tag import (
    TagFactory,
    tag_instant_delayed,
    tag_instant_traceable,
    tag_instant_analytical,
    tag_instant_functional,
)
from tests.factories.page import TaggableContentPageFactory
from wagtail_tag_manager.models import Tag


@pytest.mark.django_db
def test_view_functional(client, site):
    response = client.get(site.root_page.url)
    assert response.status_code == 200

    tag_instant_functional(tag_location=Tag.TOP_HEAD)
    client.cookies = SimpleCookie({"wtm": "functional:true"})
    response = client.get(site.root_page.url)
    assert response.status_code == 200
    assert b'console.log("functional instant")' in response.content

    tag_instant_functional(name="instant functional 2", tag_location=Tag.BOTTOM_HEAD)
    client.cookies = SimpleCookie({"wtm": "functional:true"})
    response = client.get(site.root_page.url)
    assert response.status_code == 200
    assert b'console.log("functional instant")' in response.content

    client.cookies = SimpleCookie({"wtm": "functional:false"})
    response = client.get(site.root_page.url)
    assert response.status_code == 200
    assert b'console.log("functional instant")' in response.content


@pytest.mark.django_db
def test_view_analytical(client, site):
    tag_instant_analytical(tag_location=Tag.TOP_BODY)
    client.cookies = SimpleCookie({"wtm": "analytical:true"})
    response = client.get(site.root_page.url)
    assert response.status_code == 200
    assert b'console.log("analytical instant")' in response.content


@pytest.mark.django_db
def test_view_delayed(client, site):
    tag_instant_delayed(tag_location=Tag.TOP_BODY)
    client.cookies = SimpleCookie({"wtm": "delayed:true"})
    response = client.get(site.root_page.url)
    assert response.status_code == 200
    assert b'console.log("delayed instant")' in response.content


@pytest.mark.django_db
def test_view_traceable(client, site):
    tag_instant_traceable(tag_location=Tag.BOTTOM_BODY)
    client.cookies = SimpleCookie({"wtm": "traceable:true"})
    response = client.get(site.root_page.url)
    assert response.status_code == 200
    assert b'console.log("traceable instant")' in response.content


@pytest.mark.django_db
def test_page_tags(client, site):
    response = client.get(site.root_page.url)
    assert response.status_code == 200

    tag_functional = TagFactory(
        name="functional instant",
        auto_load=False,
        tag_loading=Tag.INSTANT_LOAD,
        content='<script>console.log("functional")</script>',
    )
    tag_analytical = TagFactory(
        name="analytical instant",
        auto_load=False,
        tag_loading=Tag.INSTANT_LOAD,
        tag_type="analytical",
        content='<script>console.log("analytical")</script>',
    )
    tag_delayed = TagFactory(
        name="delayed instant",
        auto_load=False,
        tag_loading=Tag.INSTANT_LOAD,
        tag_type="delayed",
        content='<script>console.log("delayed")</script>',
    )
    tag_traceable = TagFactory(
        name="traceable instant",
        auto_load=False,
        tag_loading=Tag.INSTANT_LOAD,
        tag_type="traceable",
        content='<script>console.log("traceable")</script>',
    )

    assert tag_functional in Tag.objects.passive().sorted()
    assert tag_analytical in Tag.objects.passive().sorted()
    assert tag_delayed in Tag.objects.passive().sorted()
    assert tag_traceable in Tag.objects.passive().sorted()

    page = TaggableContentPageFactory(parent=site.root_page, slug="tagged-page")
    page.tags.add(tag_functional)
    page.tags.add(tag_analytical)
    page.tags.add(tag_delayed)
    page.tags.add(tag_traceable)
    page.save()

    client.cookies = SimpleCookie({"wtm": "functional:true"})
    response = client.get(page.get_url())
    assert response.status_code == 200
    assert b'console.log("functional")' in response.content

    client.cookies = SimpleCookie({"wtm": "analytical:true"})
    response = client.get(page.get_url())
    assert response.status_code == 200
    assert b'console.log("analytical")' in response.content

    client.cookies = SimpleCookie({"wtm": "delayed:true"})
    response = client.get(page.get_url())
    assert response.status_code == 200
    assert b'console.log("delayed")' in response.content

    client.cookies = SimpleCookie({"wtm": "traceable:true"})
    response = client.get(page.get_url())
    assert response.status_code == 200
    assert b'console.log("traceable")' in response.content
