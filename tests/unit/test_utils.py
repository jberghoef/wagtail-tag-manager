"""Robustness tests for cookie (de)serialisation.

base64_to_dict runs on the wtm cookie for every request via the consent
middleware, so a malformed cookie must degrade to defaults ({}) rather than
raise and 500 the site.
"""
import base64

import pytest

from wagtail_tag_manager.utils import base64_to_dict, dict_to_base64


def test_roundtrip():
    state = {"meta": {}, "state": {"necessary": "true"}}
    assert base64_to_dict(dict_to_base64(state)) == state


@pytest.mark.parametrize(
    "cookie",
    [
        "!!! not base64 !!!",  # binascii.Error
        base64.b64encode(b"not json").decode(),  # json.JSONDecodeError
        base64.b64encode(b"\xff\xfe").decode(),  # UnicodeDecodeError
    ],
)
def test_malformed_cookie_degrades_to_empty(cookie):
    assert base64_to_dict(cookie) == {}
