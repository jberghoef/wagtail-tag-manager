from http.cookies import SimpleCookie

import pytest

from tests.factories.tag import (
    TagFactory,
    tag_instant_marketing,
    tag_instant_necessary,
    tag_instant_statistics,
    tag_instant_preferences,
)
from tests.factories.page import TaggableContentPageFactory
from wagtail_tag_manager.models import Tag
from wagtail_tag_manager.utils import dict_to_base64


@pytest.mark.django_db
def test_view_necessary(client, site):
    response = client.get(site.root_page.url)
    assert response.status_code == 200

    tag_instant_necessary(tag_location=Tag.TOP_HEAD)
    client.cookies = SimpleCookie(
        {
            "wtm": dict_to_base64(
                {
                    "meta": {},
                    "state": {
                        "necessary": "true",
                    },
                }
            )
        }
    )
    response = client.get(site.root_page.url)
    assert response.status_code == 200
    assert b'console.log("necessary instant")' in response.content

    tag_instant_necessary(name="instant necessary 2", tag_location=Tag.BOTTOM_HEAD)
    client.cookies = SimpleCookie(
        {
            "wtm": dict_to_base64(
                {
                    "meta": {},
                    "state": {
                        "necessary": "true",
                    },
                }
            )
        }
    )
    response = client.get(site.root_page.url)
    assert response.status_code == 200
    assert b'console.log("necessary instant")' in response.content

    client.cookies = SimpleCookie(
        {
            "wtm": dict_to_base64(
                {
                    "meta": {},
                    "state": {
                        "necessary": "false",
                    },
                }
            )
        }
    )
    response = client.get(site.root_page.url)
    assert response.status_code == 200
    assert b'console.log("necessary instant")' in response.content


@pytest.mark.django_db
def test_view_preferences(client, site):
    tag_instant_preferences(tag_location=Tag.TOP_BODY)
    client.cookies = SimpleCookie(
        {
            "wtm": dict_to_base64(
                {
                    "meta": {},
                    "state": {
                        "preferences": "true",
                    },
                }
            )
        }
    )
    response = client.get(site.root_page.url)
    assert response.status_code == 200
    assert b'console.log("preferences instant")' in response.content


@pytest.mark.django_db
def test_view_statistics(client, site):
    tag_instant_statistics(tag_location=Tag.TOP_BODY)
    client.cookies = SimpleCookie(
        {
            "wtm": dict_to_base64(
                {
                    "meta": {},
                    "state": {
                        "statistics": "true",
                    },
                }
            )
        }
    )
    response = client.get(site.root_page.url)
    assert response.status_code == 200
    assert b'console.log("statistics instant")' in response.content


@pytest.mark.django_db
def test_view_marketing(client, site):
    tag_instant_marketing(tag_location=Tag.BOTTOM_BODY)
    client.cookies = SimpleCookie(
        {
            "wtm": dict_to_base64(
                {
                    "meta": {},
                    "state": {
                        "marketing": "true",
                    },
                }
            )
        }
    )
    response = client.get(site.root_page.url)
    assert response.status_code == 200
    assert b'console.log("marketing instant")' in response.content


@pytest.mark.django_db
def test_page_tags(client, site):
    response = client.get(site.root_page.url)
    assert response.status_code == 200

    tag_necessary = TagFactory(
        name="necessary instant",
        auto_load=False,
        tag_loading=Tag.INSTANT_LOAD,
        content='<script>console.log("necessary")</script>',
    )
    tag_preferences = TagFactory(
        name="preferences instant",
        auto_load=False,
        tag_loading=Tag.INSTANT_LOAD,
        tag_type="preferences",
        content='<script>console.log("preferences")</script>',
    )
    tag_statistics = TagFactory(
        name="statistics instant",
        auto_load=False,
        tag_loading=Tag.INSTANT_LOAD,
        tag_type="statistics",
        content='<script>console.log("statistics")</script>',
    )
    tag_marketing = TagFactory(
        name="marketing instant",
        auto_load=False,
        tag_loading=Tag.INSTANT_LOAD,
        tag_type="marketing",
        content='<script>console.log("marketing")</script>',
    )

    assert tag_necessary in Tag.objects.passive().sorted()
    assert tag_preferences in Tag.objects.passive().sorted()
    assert tag_statistics in Tag.objects.passive().sorted()
    assert tag_marketing in Tag.objects.passive().sorted()

    page = TaggableContentPageFactory(parent=site.root_page, slug="tagged-page")
    page.wtm_tags.add(tag_necessary)
    page.wtm_tags.add(tag_preferences)
    page.wtm_tags.add(tag_statistics)
    page.wtm_tags.add(tag_marketing)
    page.save()

    client.cookies = SimpleCookie(
        {
            "wtm": dict_to_base64(
                {
                    "meta": {},
                    "state": {
                        "necessary": "true",
                    },
                }
            )
        }
    )
    response = client.get(page.get_url())
    assert response.status_code == 200
    assert b'console.log("necessary")' in response.content

    client.cookies = SimpleCookie(
        {
            "wtm": dict_to_base64(
                {
                    "meta": {},
                    "state": {
                        "preferences": "true",
                    },
                }
            )
        }
    )
    response = client.get(page.get_url())
    assert response.status_code == 200
    assert b'console.log("preferences")' in response.content

    client.cookies = SimpleCookie(
        {
            "wtm": dict_to_base64(
                {
                    "meta": {},
                    "state": {
                        "statistics": "true",
                    },
                }
            )
        }
    )
    response = client.get(page.get_url())
    assert response.status_code == 200
    assert b'console.log("statistics")' in response.content

    client.cookies = SimpleCookie(
        {
            "wtm": dict_to_base64(
                {
                    "meta": {},
                    "state": {
                        "marketing": "true",
                    },
                }
            )
        }
    )
    response = client.get(page.get_url())
    assert response.status_code == 200
    assert b'console.log("marketing")' in response.content
