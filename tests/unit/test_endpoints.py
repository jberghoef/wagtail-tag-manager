import json
from http.cookies import SimpleCookie

import pytest

from tests.factories.tag import (
    TagFactory,
    tag_lazy_marketing,
    tag_lazy_necessary,
    tag_lazy_statistics,
    tag_lazy_preferences,
    tag_instant_marketing,
    tag_instant_statistics,
    tag_instant_preferences,
)
from tests.factories.page import TaggableContentPageFactory
from tests.factories.trigger import TriggerFactory
from wagtail_tag_manager.utils import dict_to_base64
from wagtail_tag_manager.models import Tag, Trigger
from wagtail_tag_manager.consent import ResponseConsent


@pytest.mark.django_db(transaction=True)
def test_lazy_endpoint(client, site):
    response = client.get("/wtm/lazy/")
    assert response.status_code == 400

    response = client.post("/wtm/lazy/")
    assert response.status_code == 400

    response = client.post(
        "/wtm/lazy/", json.dumps({}), content_type="application/json"
    )
    data = response.json()

    assert response.status_code == 200
    assert "tags" in data


@pytest.mark.django_db(transaction=True)
def test_lazy_cookies(client, site):
    response = client.post(
        "/wtm/lazy/", json.dumps({}), content_type="application/json"
    )
    data = response.json()

    assert response.status_code == 200
    assert "tags" in data

    assert "wtm" in response.cookies

    consent = ResponseConsent(response)
    consent_state = consent.get_state()
    assert consent_state.get("necessary", "") == "true"
    assert consent_state.get("preferences", "") == "unset"
    assert consent_state.get("statistics", "") == "unset"
    assert consent_state.get("marketing", "") == "false"


@pytest.mark.django_db(transaction=True)
def test_required_lazy_cookies(client, site):
    tag_lazy_necessary()

    response = client.post(
        "/wtm/lazy/", json.dumps({}), content_type="application/json"
    )
    data = response.json()

    assert response.status_code == 200
    assert "tags" in data
    assert len(data["tags"]) == 1

    assert "wtm" in response.cookies

    consent = ResponseConsent(response)
    consent_state = consent.get_state()
    assert consent_state.get("necessary", "") == "true"


@pytest.mark.django_db(transaction=True)
def test_initial_lazy_cookies(client, site):
    tag_instant_preferences()
    tag_lazy_preferences()

    client.cookies = SimpleCookie(
        {
            "wtm": dict_to_base64(
                {
                    "meta": {},
                    "state": {
                        "preferences": "unset",
                    },
                }
            )
        }
    )

    response = client.post(
        "/wtm/lazy/", json.dumps({}), content_type="application/json"
    )
    data = response.json()

    assert response.status_code == 200
    assert "tags" in data
    assert len(data["tags"]) == 2


@pytest.mark.django_db(transaction=True)
def test_statistics_lazy_cookies(client, site):
    tag_instant_statistics()
    tag_lazy_statistics()

    client.cookies = SimpleCookie({"wtm": ""})

    response = client.post(
        "/wtm/lazy/", json.dumps({}), content_type="application/json"
    )
    data = response.json()

    assert response.status_code == 200
    assert "tags" in data
    assert len(data["tags"]) == 0

    assert "wtm" in response.cookies

    consent = ResponseConsent(response)
    consent_state = consent.get_state()
    assert consent_state.get("statistics", "") == "unset"


@pytest.mark.django_db(transaction=True)
def test_generic_lazy_cookies(client, site):
    tag_instant_marketing()
    tag_lazy_marketing()

    response = client.post(
        "/wtm/lazy/", json.dumps({}), content_type="application/json"
    )
    data = response.json()

    assert response.status_code == 200
    assert "tags" in data
    assert len(data["tags"]) == 0


@pytest.mark.django_db(transaction=True)
def test_passive_tags(client, site):
    tag_necessary = TagFactory(
        name="necessary lazy",
        auto_load=False,
        tag_loading=Tag.LAZY_LOAD,
        content='<script>console.log("necessary: {{ trigger_value }}")</script>',
    )
    tag_preferences = TagFactory(
        name="preferences lazy",
        auto_load=False,
        tag_loading=Tag.LAZY_LOAD,
        tag_type="preferences",
        content='<script>console.log("preferences: {{ trigger_value }}")</script>',
    )
    tag_statistics = TagFactory(
        name="statistics lazy",
        auto_load=False,
        tag_loading=Tag.LAZY_LOAD,
        tag_type="statistics",
        content='<script>console.log("statistics: {{ trigger_value }}")</script>',
    )
    tag_marketing = TagFactory(
        name="marketing lazy",
        auto_load=False,
        tag_loading=Tag.LAZY_LOAD,
        tag_type="marketing",
        content='<script>console.log("marketing: {{ trigger_value }}")</script>',
    )

    assert tag_necessary in Tag.objects.passive().sorted()
    assert tag_preferences in Tag.objects.passive().sorted()
    assert tag_statistics in Tag.objects.passive().sorted()
    assert tag_marketing in Tag.objects.passive().sorted()

    trigger = TriggerFactory()
    trigger.tags.add(tag_necessary)
    trigger.tags.add(tag_preferences)
    trigger.tags.add(tag_statistics)
    trigger.tags.add(tag_marketing)

    response = client.post(
        "/wtm/lazy/",
        json.dumps({"pathname": "/", "search": ""}),
        content_type="application/json",
    )
    data = response.json()

    assert response.status_code == 200
    assert "tags" in data
    assert len(data["tags"]) == 0

    response = client.post(
        "/wtm/lazy/",
        json.dumps(
            {
                "pathname": "/",
                "search": "",
                "trigger": {
                    "slug": "trigger",
                    "type": Trigger.TYPE_FORM_SUBMIT,
                    "value": "1",
                },
            }
        ),
        content_type="application/json",
    )
    data = response.json()

    assert response.status_code == 200
    assert "tags" in data
    assert 'console.log("necessary: 1")' in data["tags"][0]["string"]

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
    response = client.post(
        "/wtm/lazy/",
        json.dumps(
            {
                "pathname": "/",
                "search": "",
                "trigger": {
                    "slug": "trigger",
                    "type": Trigger.TYPE_FORM_SUBMIT,
                    "value": "2",
                },
            }
        ),
        content_type="application/json",
    )
    data = response.json()

    assert response.status_code == 200
    assert "tags" in data
    assert 'console.log("preferences: 2")' in data["tags"][1]["string"]

    client.cookies = SimpleCookie(
        {
            "wtm": dict_to_base64(
                {
                    "meta": {},
                    "state": {
                        "preferences": "false",
                        "statistics": "true",
                    },
                }
            )
        }
    )
    response = client.post(
        "/wtm/lazy/",
        json.dumps(
            {
                "pathname": "/",
                "search": "",
                "trigger": {
                    "slug": "trigger",
                    "type": Trigger.TYPE_FORM_SUBMIT,
                    "value": "3",
                },
            }
        ),
        content_type="application/json",
    )
    data = response.json()

    assert response.status_code == 200
    assert "tags" in data
    assert 'console.log("statistics: 3")' in data["tags"][1]["string"]

    client.cookies = SimpleCookie(
        {
            "wtm": dict_to_base64(
                {
                    "meta": {},
                    "state": {
                        "preferences": "false",
                        "marketing": "true",
                    },
                }
            )
        }
    )
    response = client.post(
        "/wtm/lazy/",
        json.dumps(
            {
                "pathname": "/",
                "search": "",
                "trigger": {
                    "slug": "trigger",
                    "type": Trigger.TYPE_FORM_SUBMIT,
                    "value": "4",
                },
            }
        ),
        content_type="application/json",
    )
    data = response.json()

    assert response.status_code == 200
    assert "tags" in data
    assert 'console.log("marketing: 4")' in data["tags"][1]["string"]


@pytest.mark.django_db(transaction=True)
def test_page_tags(client, site):
    tag_necessary = TagFactory(
        name="necessary lazy",
        auto_load=False,
        tag_loading=Tag.LAZY_LOAD,
        content='<script>console.log("necessary")</script>',
    )
    tag_preferences = TagFactory(
        name="preferences lazy",
        auto_load=False,
        tag_loading=Tag.LAZY_LOAD,
        tag_type="preferences",
        content='<script>console.log("preferences")</script>',
    )
    tag_statistics = TagFactory(
        name="statistics lazy",
        auto_load=False,
        tag_loading=Tag.LAZY_LOAD,
        tag_type="statistics",
        content='<script>console.log("statistics")</script>',
    )
    tag_marketing = TagFactory(
        name="marketing lazy",
        auto_load=False,
        tag_loading=Tag.LAZY_LOAD,
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

    assert len(page.wtm_tags.all()) == 4

    response = client.post(
        "/wtm/lazy/",
        json.dumps({"pathname": page.get_url()}),
        content_type="application/json",
    )
    data = response.json()

    assert response.status_code == 200
    assert "tags" in data
    results = ['console.log("necessary")', 'console.log("preferences")']
    for tag in data.get("tags", []):
        assert tag["string"].strip() in results

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
    response = client.post(
        "/wtm/lazy/",
        json.dumps({"pathname": page.get_url()}),
        content_type="application/json",
    )
    data = response.json()

    assert response.status_code == 200
    assert "tags" in data
    results = ['console.log("necessary")', 'console.log("preferences")']
    for tag in data.get("tags", []):
        assert tag["string"].strip() in results

    client.cookies = SimpleCookie(
        {
            "wtm": dict_to_base64(
                {
                    "meta": {},
                    "state": {
                        "preferences": "false",
                        "statistics": "true",
                    },
                }
            )
        }
    )
    response = client.post(
        "/wtm/lazy/",
        json.dumps({"pathname": page.get_url()}),
        content_type="application/json",
    )
    data = response.json()

    assert response.status_code == 200
    assert "tags" in data
    results = ['console.log("necessary")', 'console.log("statistics")']
    for tag in data.get("tags", []):
        assert tag["string"].strip() in results

    client.cookies = SimpleCookie(
        {
            "wtm": dict_to_base64(
                {
                    "meta": {},
                    "state": {
                        "preferences": "false",
                        "marketing": "true",
                    },
                }
            )
        }
    )
    response = client.post(
        "/wtm/lazy/",
        json.dumps({"pathname": page.get_url()}),
        content_type="application/json",
    )
    data = response.json()

    assert response.status_code == 200
    assert "tags" in data
    results = ['console.log("necessary")', 'console.log("marketing")']
    for tag in data.get("tags", []):
        assert tag["string"].strip() in results
