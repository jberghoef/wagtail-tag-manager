import json
import uuid
from datetime import datetime
from http.cookies import SimpleCookie

import pytest
from freezegun import freeze_time

from wagtail_tag_manager.consent import Consent, ResponseConsent
from wagtail_tag_manager.utils import dict_to_base64
from wagtail_tag_manager.models import CookieConsent
from wagtail_tag_manager.settings import CookieConsentSettings


@pytest.mark.django_db
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


@pytest.mark.django_db
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


@pytest.mark.django_db
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


@pytest.mark.django_db
def test_consent_invalidated_when_conditions_page_changes(rf, site):
    # If the privacy/conditions page is published *after* a user consented,
    # their prior consent must be treated as invalid (reset to defaults).
    page = site.root_page
    page.last_published_at = datetime(2020, 6, 1)  # naive: settings has USE_TZ=False
    page.save()

    consent_settings = CookieConsentSettings.for_site(site)
    consent_settings.conditions_page = page
    consent_settings.save()

    identifier = uuid.uuid4()

    def necessary_state_for(consent_time):
        CookieConsent.objects.filter(identifier=identifier).delete()
        with freeze_time(consent_time):
            CookieConsent.objects.create(
                identifier=identifier, consent_state="necessary: true;", location="/"
            )
        request = rf.get("/")
        request.COOKIES = {
            "wtm": dict_to_base64(
                {"meta": {"id": str(identifier)}, "state": {"necessary": "true"}}
            )
        }
        return Consent(request).get_state()["necessary"]

    # Consent given AFTER the page was last published -> still valid.
    assert necessary_state_for("2020-12-01") == "true"
    # Consent given BEFORE the page was last published -> invalidated.
    assert necessary_state_for("2020-01-01") == "unset"
