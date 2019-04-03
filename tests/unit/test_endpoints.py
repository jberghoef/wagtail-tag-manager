import json
from http.cookies import SimpleCookie

import pytest

from tests.factories.tag import (
    TagFactory,
    tag_lazy_traceable,
    tag_lazy_analytical,
    tag_lazy_functional,
    tag_lazy_continue,
    tag_instant_traceable,
    tag_instant_analytical,
    tag_instant_continue,
)
from tests.factories.trigger import TriggerFactory
from wagtail_tag_manager.models import Tag
from wagtail_tag_manager.utils import get_consent


@pytest.mark.django_db
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


@pytest.mark.django_db
def test_lazy_cookies(client, site):
    response = client.post(
        "/wtm/lazy/", json.dumps({}), content_type="application/json"
    )
    data = response.json()

    assert response.status_code == 200
    assert "tags" in data

    assert "wtm" in response.cookies
    consent_state = get_consent(response)
    assert consent_state.get("functional", "") == "true"
    assert consent_state.get("analytical", "") == "unset"
    assert consent_state.get("continue", "") == "true"
    assert consent_state.get("traceable", "") == "false"


@pytest.mark.django_db
def test_required_lazy_cookies(client, site):
    tag_lazy_functional()

    response = client.post(
        "/wtm/lazy/", json.dumps({}), content_type="application/json"
    )
    data = response.json()

    assert response.status_code == 200
    assert "tags" in data
    assert len(data["tags"]) == 1

    assert "wtm" in response.cookies
    consent_state = get_consent(response)
    assert consent_state.get("functional", "") == "true"


@pytest.mark.django_db
def test_initial_lazy_cookies(client, site):
    tag_instant_analytical()
    tag_lazy_analytical()

    client.cookies = SimpleCookie({"wtm": "analytical:unset"})

    response = client.post(
        "/wtm/lazy/", json.dumps({}), content_type="application/json"
    )
    data = response.json()

    assert response.status_code == 200
    assert "tags" in data
    assert len(data["tags"]) == 2


@pytest.mark.django_db
def test_continue_lazy_cookies(client, site):
    tag_instant_continue()
    tag_lazy_continue()

    client.cookies = SimpleCookie({"wtm": ""})

    response = client.post(
        "/wtm/lazy/", json.dumps({}), content_type="application/json"
    )
    data = response.json()

    assert response.status_code == 200
    assert "tags" in data
    assert len(data["tags"]) == 0

    assert "wtm" in response.cookies
    consent_state = get_consent(response)

    assert consent_state.get("continue", "") == "true"


@pytest.mark.django_db
def test_generic_lazy_cookies(client, site):
    tag_instant_traceable()
    tag_lazy_traceable()

    response = client.post(
        "/wtm/lazy/", json.dumps({}), content_type="application/json"
    )
    data = response.json()

    assert response.status_code == 200
    assert "tags" in data
    assert len(data["tags"]) == 0


@pytest.mark.django_db
def test_passive_tags(client, site):
    tag_functional = TagFactory(
        name="functional lazy",
        auto_load=False,
        tag_loading=Tag.LAZY_LOAD,
        content='<script>console.log("functional: {{ state }}")</script>',
    )
    tag_analytical = TagFactory(
        name="analytical lazy",
        auto_load=False,
        tag_loading=Tag.LAZY_LOAD,
        tag_type="analytical",
        content='<script>console.log("analytical: {{ state }}")</script>',
    )
    tag_continue = TagFactory(
        name="continue lazy",
        auto_load=False,
        tag_loading=Tag.LAZY_LOAD,
        tag_type="continue",
        content='<script>console.log("continue: {{ state }}")</script>',
    )
    tag_traceable = TagFactory(
        name="traceable lazy",
        auto_load=False,
        tag_loading=Tag.LAZY_LOAD,
        tag_type="traceable",
        content='<script>console.log("traceable: {{ state }}")</script>',
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

    response = client.post(
        "/wtm/lazy/",
        json.dumps({"pathname": "/", "search": ""}),
        content_type="application/json",
    )
    data = response.json()

    assert response.status_code == 200
    assert "tags" in data
    assert len(data["tags"]) == 0

    trigger.tags.add(tag_analytical)
    response = client.post(
        "/wtm/lazy/",
        json.dumps({"pathname": "/", "search": "?state=1"}),
        content_type="application/json",
    )
    data = response.json()

    assert response.status_code == 200
    assert "tags" in data
    assert 'console.log("functional: 1")' in data["tags"][0]["string"]

    client.cookies = SimpleCookie({"wtm": "analytical:true"})
    response = client.post(
        "/wtm/lazy/",
        json.dumps({"pathname": "/", "search": "?state=2"}),
        content_type="application/json",
    )
    data = response.json()

    assert response.status_code == 200
    assert "tags" in data
    assert 'console.log("analytical: 2")' in data["tags"][1]["string"]

    client.cookies = SimpleCookie({"wtm": "analytical:false|continue:true"})
    response = client.post(
        "/wtm/lazy/",
        json.dumps({"pathname": "/", "search": "?state=3"}),
        content_type="application/json",
    )
    data = response.json()

    assert response.status_code == 200
    assert "tags" in data
    assert 'console.log("continue: 3")' in data["tags"][1]["string"]

    client.cookies = SimpleCookie({"wtm": "analytical:false|traceable:true"})
    response = client.post(
        "/wtm/lazy/",
        json.dumps({"pathname": "/", "search": "?state=4"}),
        content_type="application/json",
    )
    data = response.json()

    assert response.status_code == 200
    assert "tags" in data
    assert 'console.log("traceable: 4")' in data["tags"][1]["string"]
