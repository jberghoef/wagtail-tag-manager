from http.cookies import SimpleCookie

import pytest

from tests.factories.tag import (
    TagFactory,
    tag_instant_traceable,
    tag_instant_analytical,
    tag_instant_continue,
    tag_instant_functional,
)
from tests.factories.trigger import TriggerFactory
from wagtail_tag_manager.models import Tag


@pytest.mark.django_db
def test_view_functional(client, site):
    response = client.get(site.root_page.url)
    assert response.status_code == 200

    tag_instant_functional(tag_location=Tag.TOP_HEAD)
    client.cookies = SimpleCookie({"wtm_functional": "true"})
    response = client.get(site.root_page.url)
    assert response.status_code == 200
    assert b'console.log("functional instant")' in response.content

    tag_instant_functional(name="instant functional 2", tag_location=Tag.BOTTOM_HEAD)
    client.cookies = SimpleCookie({"wtm_functional": "true"})
    response = client.get(site.root_page.url)
    assert response.status_code == 200
    assert b'console.log("functional instant")' in response.content

    client.cookies = SimpleCookie({"wtm_functional": "false"})
    response = client.get(site.root_page.url)
    assert response.status_code == 200
    assert b'console.log("functional instant")' in response.content


@pytest.mark.django_db
def test_view_analytical(client, site):
    tag_instant_analytical(tag_location=Tag.TOP_BODY)
    client.cookies = SimpleCookie({"wtm_analytical": "true"})
    response = client.get(site.root_page.url)
    assert response.status_code == 200
    assert b'console.log("analytical instant")' in response.content


@pytest.mark.django_db
def test_view_continue(client, site):
    tag_instant_continue(tag_location=Tag.TOP_BODY)
    client.cookies = SimpleCookie({"wtm_continue": "true"})
    response = client.get(site.root_page.url)
    assert response.status_code == 200
    assert b'console.log("continue instant")' in response.content


@pytest.mark.django_db
def test_view_traceable(client, site):
    tag_instant_traceable(tag_location=Tag.BOTTOM_BODY)
    client.cookies = SimpleCookie({"wtm_traceable": "true"})
    response = client.get(site.root_page.url)
    assert response.status_code == 200
    assert b'console.log("traceable instant")' in response.content


@pytest.mark.django_db
def test_passive_view(client, site):
    response = client.get(site.root_page.url)
    assert response.status_code == 200

    tag_functional = TagFactory(
        name="functional lazy",
        active=False,
        tag_loading=Tag.INSTANT_LOAD,
        content='<script>console.log("{{ state }}")</script>',
    )
    tag_analytical = TagFactory(
        name="analytical lazy",
        active=False,
        tag_loading=Tag.INSTANT_LOAD,
        tag_type="analytical",
        content='<script>console.log("{{ state }}")</script>',
    )
    tag_continue = TagFactory(
        name="continue lazy",
        active=False,
        tag_loading=Tag.INSTANT_LOAD,
        tag_type="continue",
        content='<script>console.log("{{ state }}")</script>',
    )
    tag_traceable = TagFactory(
        name="traceable lazy",
        active=False,
        tag_loading=Tag.INSTANT_LOAD,
        tag_type="traceable",
        content='<script>console.log("{{ state }}")</script>',
    )

    assert tag_functional in Tag.objects.passive().sorted()
    assert tag_analytical in Tag.objects.passive().sorted()
    assert tag_continue in Tag.objects.passive().sorted()
    assert tag_traceable in Tag.objects.passive().sorted()

    trigger = TriggerFactory(pattern="[?&]state=(?P<state>\S+)")
    trigger.tags.add(tag_functional)
    trigger.tags.add(tag_analytical)
    trigger.tags.add(tag_continue)
    trigger.tags.add(tag_traceable)

    client.cookies = SimpleCookie({"wtm_functional": "true"})
    response = client.get("/?state=1")
    assert response.status_code == 200
    assert b'console.log("1")' in response.content

    client.cookies = SimpleCookie({"wtm_analytical": "true"})
    response = client.get("/?state=2")
    assert response.status_code == 200
    assert b'console.log("2")' in response.content

    client.cookies = SimpleCookie({"wtm_continue": "true"})
    response = client.get("/?state=3")
    assert response.status_code == 200
    assert b'console.log("3")' in response.content

    client.cookies = SimpleCookie({"wtm_traceable": "true"})
    response = client.get("/?state=4")
    assert response.status_code == 200
    assert b'console.log("4")' in response.content
