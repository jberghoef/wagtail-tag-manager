import pytest

from src.wagtail_tag_manager.utils import parse_consent_state


def test_consent_result(live_server, browser):
    browser.get(live_server.url)

    wtm_cookie = None
    for cookie in browser.get_cookies():
        if cookie.get("name", "") == "wtm":
            wtm_cookie = cookie

    consent_state = parse_consent_state(wtm_cookie.get("value"))
    assert consent_state.get("functional") == "true"
    assert consent_state.get("analytical") == "unset"
    assert consent_state.get("continue") == "unset"
    assert consent_state.get("traceable") == "unset"
