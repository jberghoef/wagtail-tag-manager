import json
from http.cookies import SimpleCookie

import pytest

from wagtail_tag_manager.consent import ResponseConsent


@pytest.mark.django_db(transaction=True)
def test_handles_malformed_consent(client, site):
    client.cookies = SimpleCookie({"wtm": "malformed"})

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
    assert consent_state.get("necessary", "") == "true"
    assert consent_state.get("preferences", "") == "unset"
    assert consent_state.get("statistics", "") == "unset"
    assert consent_state.get("marketing", "") == "false"


@pytest.mark.django_db(transaction=True)
def test_upgrades_legacy_consent_state(client, site):
    client.cookies = SimpleCookie(
        {"wtm": "necessary:true|preferences:unset|statistics:pending|marketing:false"},
    )

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
    assert consent_state.get("necessary", "") == "true"
    assert consent_state.get("preferences", "") == "unset"
    assert consent_state.get("statistics", "") == "pending"
    assert consent_state.get("marketing", "") == "false"


@pytest.mark.django_db(transaction=True)
def test_upgrades_legacy_consent_meta(client, site):
    client.cookies = SimpleCookie(
        {
            "wtm": "necessary:true|preferences:unset|statistics:pending|marketing:false",
            "wtm_id": "123",
        },
    )

    response = client.post(
        "/wtm/lazy/", json.dumps({}), content_type="application/json"
    )
    data = response.json()

    assert response.status_code == 200
    assert "tags" in data
    assert len(data["tags"]) == 0

    assert "wtm" in response.cookies

    consent = ResponseConsent(response)
    consent_meta = consent.get_meta()
    assert consent_meta.get("id", "") == "123"
