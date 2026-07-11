"""Tests for the core TagStrategy decision engine (strategy.py).

These assert *intended* consent behaviour derived from the ePrivacy/GDPR model
documented in the README, not whatever the implementation happens to emit. In
particular the "delayed" load setting has a two-request lifecycle
(``unset -> pending -> true``) that is the whole point of delayed loading, so
every delayed test asserts both the resulting cookie state AND tag presence
across the transition rather than a single snapshot.

In tests/settings.py the tag types are configured as:
    necessary  -> required
    preferences -> initial
    statistics -> delayed   <-- exercised here
    marketing  -> "" (default)
"""
from http.cookies import SimpleCookie

import pytest

from tests.factories.tag import (
    tag_lazy_statistics,
    tag_instant_marketing,
    tag_instant_statistics,
)
from tests.factories.page import TaggableContentPageFactory
from wagtail_tag_manager.models import Tag
from wagtail_tag_manager.utils import dict_to_base64
from wagtail_tag_manager.consent import ResponseConsent


def _cookie(state):
    return SimpleCookie({"wtm": dict_to_base64({"meta": {}, "state": state})})


# --- Delayed lifecycle on GET (instant tags via the middleware) -------------
#
# Spec: a delayed tag must NOT load on the first visit. The first GET promotes
# consent unset -> pending (no tag yet); a subsequent GET promotes pending ->
# true and only then injects the tag instantly.


@pytest.mark.django_db
def test_delayed_first_get_sets_pending_and_withholds_tag(client, site):
    tag_instant_statistics(tag_location=Tag.TOP_BODY)

    # No wtm cookie -> consent is unset.
    response = client.get(site.root_page.url)

    assert response.status_code == 200
    # The delayed tag must be withheld on the very first visit.
    assert b'console.log("statistics instant")' not in response.content
    # ...but consent must advance to `pending` so the *next* visit can load it.
    assert ResponseConsent(response).get_state().get("statistics") == "pending"


@pytest.mark.django_db
def test_delayed_promotes_pending_to_true_and_loads_tag(client, site):
    tag_instant_statistics(tag_location=Tag.TOP_BODY)

    client.cookies = _cookie({"statistics": "pending"})
    response = client.get(site.root_page.url)

    assert response.status_code == 200
    # On the second visit the delayed tag now loads...
    assert b'console.log("statistics instant")' in response.content
    # ...and consent is promoted to a settled `true`.
    assert ResponseConsent(response).get_state().get("statistics") == "true"


@pytest.mark.django_db
def test_delayed_true_keeps_loading_tag(client, site):
    tag_instant_statistics(tag_location=Tag.TOP_BODY)

    client.cookies = _cookie({"statistics": "true"})
    response = client.get(site.root_page.url)

    assert response.status_code == 200
    assert b'console.log("statistics instant")' in response.content
    assert ResponseConsent(response).get_state().get("statistics") == "true"


# --- Delayed lifecycle on POST (lazy endpoint) ------------------------------
#
# Spec: the lazy endpoint must NOT advance the lifecycle. It only loads the tag
# once consent has already settled to `true` (which happens on a GET). While
# `pending`, a POST must hold: no tag, state unchanged.


@pytest.mark.django_db
def test_delayed_lazy_pending_holds_and_stays_pending(client, site):
    tag_lazy_statistics()

    client.cookies = _cookie({"statistics": "pending"})
    response = client.post(
        "/wtm/lazy/", "{}", content_type="application/json"
    )

    assert response.status_code == 200
    assert len(response.json()["tags"]) == 0
    # The lazy endpoint must not promote pending -> true; only a GET does that.
    assert ResponseConsent(response).get_state().get("statistics") == "pending"


@pytest.mark.django_db
def test_delayed_lazy_true_loads_tag(client, site):
    tag_lazy_statistics()

    client.cookies = _cookie({"statistics": "true"})
    response = client.post(
        "/wtm/lazy/", "{}", content_type="application/json"
    )

    assert response.status_code == 200
    tags = response.json()["tags"]
    assert any('console.log("statistics lazy")' in (t["string"] or "") for t in tags)
    assert ResponseConsent(response).get_state().get("statistics") == "true"


# --- Page tag inheritance via wtm_include_children --------------------------
#
# Spec: a page marked wtm_include_children propagates its own tags down to
# descendant pages; without the flag, descendants do not inherit them.


def _build_taggable_pair(root):
    """Build a fresh parent/child pair of taggable pages under `root`.

    Self-contained rather than reaching into the shared `site` fixture tree, so
    the inheritance tests can't break silently if that fixture changes.
    """
    parent = TaggableContentPageFactory(parent=root, slug="wtm-inherit-parent")
    child = TaggableContentPageFactory(parent=parent, slug="wtm-inherit-child")
    return parent, child


@pytest.mark.django_db
def test_child_inherits_parent_tags_when_include_children(client, site):
    from tests.factories.tag import tag_instant_necessary

    parent, child = _build_taggable_pair(site.root_page)
    parent.wtm_include_children = True
    # required type -> consent never hides it; auto_load=False -> it can ONLY
    # reach the child through the parent relationship, isolating inheritance.
    parent.wtm_tags.add(
        tag_instant_necessary(tag_location=Tag.TOP_HEAD, auto_load=False)
    )
    parent.save()  # ParentalManyToManyField: add() is in-memory until save()

    response = client.get(child.url)

    assert response.status_code == 200
    assert b'console.log("necessary instant")' in response.content


@pytest.mark.django_db
def test_child_does_not_inherit_without_include_children(client, site):
    from tests.factories.tag import tag_instant_necessary

    parent, child = _build_taggable_pair(site.root_page)
    # Default: wtm_include_children is False. auto_load=False so the only way it
    # could appear on the child is via (disabled) inheritance.
    parent.wtm_tags.add(
        tag_instant_necessary(tag_location=Tag.TOP_HEAD, auto_load=False)
    )
    parent.save()  # ParentalManyToManyField: add() is in-memory until save()

    response = client.get(child.url)

    assert response.status_code == 200
    assert b'console.log("necessary instant")' not in response.content


# --- Debug mode -------------------------------------------------------------
#
# Spec: with the wtm_debug cookie set, every tag loads regardless of consent so
# an editor can preview them. A default (marketing) tag would normally be
# withheld while consent is unset.


@pytest.mark.django_db
def test_debug_cookie_loads_tags_regardless_of_consent(client, site):
    tag_instant_marketing(tag_location=Tag.BOTTOM_BODY)

    # Sanity: without debug and no consent, the marketing tag is withheld.
    baseline = client.get(site.root_page.url)
    assert b'console.log("marketing instant")' not in baseline.content

    client.cookies = SimpleCookie({"wtm_debug": "true"})
    response = client.get(site.root_page.url)

    assert response.status_code == 200
    assert b'console.log("marketing instant")' in response.content
