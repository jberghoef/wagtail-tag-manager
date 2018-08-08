import json

import pytest
from http.cookies import SimpleCookie

from tests.factories.tag import (
    tag_instant_traceable, tag_instant_analytical, tag_instant_functional,
    tag_lazy_traceable, tag_lazy_analytical, tag_lazy_functional)


@pytest.mark.django_db
def test_lazy_endpoint(client, site):
    response = client.get('/wtm/lazy/')
    assert response.status_code == 400

    response = client.post('/wtm/lazy/')
    assert response.status_code == 400

    response = client.post(
        '/wtm/lazy/', json.dumps({}), content_type="application/json")
    data = response.json()

    assert response.status_code == 200
    assert 'tags' in data


@pytest.mark.django_db
def test_lazy_cookies(client, site):
    response = client.post(
        '/wtm/lazy/',
        json.dumps({}),
        content_type="application/json")
    data = response.json()

    assert response.status_code == 200
    assert 'tags' in data

    assert 'wtm_functional' in response.cookies
    assert response.cookies.get('wtm_functional').value == 'true'
    assert 'wtm_analytical' not in response.cookies
    assert 'wtm_traceable' not in response.cookies

    response = client.post(
        '/wtm/lazy/',
        json.dumps({'consent': False}),
        content_type="application/json")
    data = response.json()

    assert response.status_code == 200
    assert 'tags' in data

    assert 'wtm_functional' in response.cookies
    assert response.cookies.get('wtm_functional').value == 'true'
    assert 'wtm_analytical' in response.cookies
    assert response.cookies.get('wtm_analytical').value == 'false'
    assert 'wtm_traceable' in response.cookies
    assert response.cookies.get('wtm_traceable').value == 'false'

    response = client.post(
        '/wtm/lazy/',
        json.dumps({'consent': True}),
        content_type="application/json")
    data = response.json()

    assert response.status_code == 200
    assert 'tags' in data

    assert 'wtm_functional' in response.cookies
    assert response.cookies.get('wtm_functional').value == 'true'
    assert 'wtm_analytical' in response.cookies
    assert response.cookies.get('wtm_analytical').value == 'true'
    assert 'wtm_traceable' in response.cookies
    assert response.cookies.get('wtm_traceable').value == 'true'


@pytest.mark.django_db
def test_required_lazy_cookies(client, site):
    tag_lazy_functional()

    response = client.post(
        '/wtm/lazy/',
        json.dumps({}),
        content_type="application/json")
    data = response.json()

    assert response.status_code == 200
    assert 'tags' in data
    assert len(data['tags']) == 1

    assert 'wtm_functional' in response.cookies
    assert response.cookies.get('wtm_functional').value == 'true'

    response = client.post(
        '/wtm/lazy/',
        json.dumps({'consent': False}),
        content_type="application/json")
    data = response.json()

    assert response.status_code == 200
    assert 'tags' in data
    assert len(data['tags']) == 1

    assert 'wtm_functional' in response.cookies
    assert response.cookies.get('wtm_functional').value == 'true'


@pytest.mark.django_db
def test_initial_lazy_cookies(client, site):
    tag_instant_analytical()
    tag_lazy_analytical()

    client.cookies = SimpleCookie({'wtm_analytical': 'unset'})

    response = client.post(
        '/wtm/lazy/',
        json.dumps({}),
        content_type="application/json")
    data = response.json()

    assert response.status_code == 200
    assert 'tags' in data
    assert len(data['tags']) == 2

    response = client.post(
        '/wtm/lazy/',
        json.dumps({'consent': False}),
        content_type="application/json")
    data = response.json()

    assert response.status_code == 200
    assert 'tags' in data
    assert len(data['tags']) == 0

    assert 'wtm_analytical' in response.cookies
    assert response.cookies.get('wtm_analytical').value == 'false'

    response = client.post(
        '/wtm/lazy/',
        json.dumps({'consent': True}),
        content_type="application/json")
    data = response.json()

    assert response.status_code == 200
    assert 'tags' in data
    assert len(data['tags']) == 2

    assert 'wtm_analytical' in response.cookies
    assert response.cookies.get('wtm_analytical').value == 'true'


@pytest.mark.django_db
def test_generic_lazy_cookies(client, site):
    tag_instant_traceable()
    tag_lazy_traceable()

    response = client.post(
        '/wtm/lazy/',
        json.dumps({}),
        content_type="application/json")
    data = response.json()

    assert response.status_code == 200
    assert 'tags' in data
    assert len(data['tags']) == 0

    response = client.post(
        '/wtm/lazy/',
        json.dumps({'consent': False}),
        content_type="application/json")
    data = response.json()

    assert response.status_code == 200
    assert 'tags' in data
    assert len(data['tags']) == 0

    assert 'wtm_traceable' in response.cookies
    assert response.cookies.get('wtm_traceable').value == 'false'

    response = client.post(
        '/wtm/lazy/',
        json.dumps({'consent': True}),
        content_type="application/json")
    data = response.json()

    assert response.status_code == 200
    assert 'tags' in data
    assert len(data['tags']) == 2

    assert 'wtm_traceable' in response.cookies
    assert response.cookies.get('wtm_traceable').value == 'true'
