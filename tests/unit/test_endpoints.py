import json
from http.cookies import SimpleCookie

import pytest

from tests.factories.tag import (
    tag_lazy_traceable,
    tag_lazy_analytical,
    tag_lazy_functional,
    tag_instant_traceable,
    tag_instant_analytical,
    TagFactory,
)
from tests.factories.trigger import TriggerFactory

from wagtail_tag_manager.models import Tag


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

    assert "wtm_functional" in response.cookies
    assert response.cookies.get("wtm_functional").value == "true"
    assert "wtm_analytical" not in response.cookies
    assert "wtm_traceable" not in response.cookies

    client.cookies["wtm_functional"] = "false"
    response = client.post(
        "/wtm/lazy/", json.dumps({"consent": False}), content_type="application/json"
    )
    data = response.json()

    assert response.status_code == 200
    assert "tags" in data

    assert "wtm_functional" in response.cookies
    assert response.cookies.get("wtm_functional").value == "true"
    assert "wtm_analytical" in response.cookies
    assert response.cookies.get("wtm_analytical").value == "false"
    assert "wtm_traceable" in response.cookies
    assert response.cookies.get("wtm_traceable").value == "false"

    client.cookies["wtm_functional"] = "false"
    response = client.post(
        "/wtm/lazy/", json.dumps({"consent": True}), content_type="application/json"
    )
    data = response.json()

    assert response.status_code == 200
    assert "tags" in data

    assert "wtm_functional" in response.cookies
    assert response.cookies.get("wtm_functional").value == "true"
    assert "wtm_analytical" in response.cookies
    assert response.cookies.get("wtm_analytical").value == "true"
    assert "wtm_traceable" in response.cookies
    assert response.cookies.get("wtm_traceable").value == "true"


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

    assert "wtm_functional" in response.cookies
    assert response.cookies.get("wtm_functional").value == "true"

    client.cookies["wtm_functional"] = "false"
    response = client.post(
        "/wtm/lazy/", json.dumps({"consent": False}), content_type="application/json"
    )
    data = response.json()

    assert response.status_code == 200
    assert "tags" in data
    assert len(data["tags"]) == 0

    assert "wtm_functional" in response.cookies
    assert response.cookies.get("wtm_functional").value == "true"


@pytest.mark.django_db
def test_initial_lazy_cookies(client, site):
    tag_instant_analytical()
    tag_lazy_analytical()

    client.cookies = SimpleCookie({"wtm_analytical": "unset"})

    response = client.post(
        "/wtm/lazy/", json.dumps({}), content_type="application/json"
    )
    data = response.json()

    assert response.status_code == 200
    assert "tags" in data
    assert len(data["tags"]) == 2

    response = client.post(
        "/wtm/lazy/", json.dumps({"consent": False}), content_type="application/json"
    )
    data = response.json()

    assert response.status_code == 200
    assert "tags" in data
    assert len(data["tags"]) == 0

    assert "wtm_analytical" in response.cookies
    assert response.cookies.get("wtm_analytical").value == "false"

    response = client.post(
        "/wtm/lazy/", json.dumps({"consent": True}), content_type="application/json"
    )
    data = response.json()

    assert response.status_code == 200
    assert "tags" in data
    assert len(data["tags"]) == 2

    assert "wtm_analytical" in response.cookies
    assert response.cookies.get("wtm_analytical").value == "true"


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

    response = client.post(
        "/wtm/lazy/", json.dumps({"consent": False}), content_type="application/json"
    )
    data = response.json()

    assert response.status_code == 200
    assert "tags" in data
    assert len(data["tags"]) == 0

    assert "wtm_traceable" in response.cookies
    assert response.cookies.get("wtm_traceable").value == "false"

    response = client.post(
        "/wtm/lazy/", json.dumps({"consent": True}), content_type="application/json"
    )
    data = response.json()

    assert response.status_code == 200
    assert "tags" in data
    assert len(data["tags"]) == 2

    assert "wtm_traceable" in response.cookies
    assert response.cookies.get("wtm_traceable").value == "true"


@pytest.mark.django_db
def test_passive_tags(client, site):
    tag_functional = TagFactory(
        name="functional lazy",
        active=False,
        tag_loading=Tag.LAZY_LOAD,
        content='<script>console.log("{{ state }}")</script>',
    )
    tag_analytical = TagFactory(
        name="analytical lazy",
        active=False,
        tag_loading=Tag.LAZY_LOAD,
        tag_type="analytical",
        content='<script>console.log("{{ state }}")</script>',
    )
    tag_traceable = TagFactory(
        name="traceable lazy",
        active=False,
        tag_loading=Tag.LAZY_LOAD,
        tag_type="traceable",
        content='<script>console.log("{{ state }}")</script>',
    )

    trigger = TriggerFactory(pattern="[?&]state=(?P<state>\S+)")
    trigger.tags.add(tag_functional)
    trigger.tags.add(tag_analytical)
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

    response = client.post(
        "/wtm/lazy/",
        json.dumps({"pathname": "/", "search": "?state=1"}),
        content_type="application/json",
    )
    data = response.json()

    assert response.status_code == 200
    assert "tags" in data
    assert len(data["tags"]) == 1
    assert 'console.log("1")' in data["tags"][0]["string"]

    client.cookies = SimpleCookie({"wtm_analytical": "unset"})

    response = client.post(
        "/wtm/lazy/",
        json.dumps({"pathname": "/", "search": "?state=2"}),
        content_type="application/json",
    )
    data = response.json()

    assert response.status_code == 200
    assert "tags" in data
    assert len(data["tags"]) == 2
    assert 'console.log("2")' in data["tags"][1]["string"]

    response = client.post(
        "/wtm/lazy/",
        json.dumps({"consent": "true", "pathname": "/", "search": "?state=3"}),
        content_type="application/json",
    )
    data = response.json()

    assert response.status_code == 200
    assert "tags" in data
    assert len(data["tags"]) == 3
    assert 'console.log("3")' in data["tags"][2]["string"]
