import json

import pytest

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
        '/wtm/lazy/', json.dumps({
            'functional': True,
            'analytical': True,
            'traceable': True,
        }), content_type="application/json")
    data = response.json()

    assert response.status_code == 200
    assert 'tags' in data

    assert 'wtm_functional' in response.cookies
    assert response.cookies.get('wtm_functional').value == 'true'
    assert 'wtm_analytical' in response.cookies
    assert response.cookies.get('wtm_analytical').value == 'true'
    assert 'wtm_traceable' in response.cookies
    assert response.cookies.get('wtm_traceable').value == 'true'

    response = client.post(
        '/wtm/lazy/', json.dumps({
            'functional': False,
            'analytical': False,
            'traceable': False,
        }), content_type="application/json")
    data = response.json()

    assert response.status_code == 200
    assert 'tags' in data

    assert 'wtm_functional' in response.cookies
    assert response.cookies.get('wtm_functional').value == 'false'
    assert 'wtm_analytical' in response.cookies
    assert response.cookies.get('wtm_analytical').value == 'false'
    assert 'wtm_traceable' in response.cookies
    assert response.cookies.get('wtm_traceable').value == 'false'


@pytest.mark.django_db
def test_functional_lazy_cookies(client, site):
    tag_instant_functional()
    tag_lazy_functional()

    response = client.post(
        '/wtm/lazy/', json.dumps({
            'functional': True,
        }), content_type="application/json")
    data = response.json()

    assert response.status_code == 200
    assert 'tags' in data
    assert len(data['tags']) == 2

    assert 'wtm_functional' in response.cookies
    assert response.cookies.get('wtm_functional').value == 'true'

    response = client.post(
        '/wtm/lazy/', json.dumps({
            'functional': False,
        }), content_type="application/json")
    data = response.json()

    assert response.status_code == 200
    assert 'tags' in data
    assert len(data['tags']) == 0

    assert 'wtm_functional' in response.cookies
    assert response.cookies.get('wtm_functional').value == 'false'


@pytest.mark.django_db
def test_analytical_lazy_cookies(client, site):
    tag_instant_analytical()
    tag_lazy_analytical()

    response = client.post(
        '/wtm/lazy/', json.dumps({
            'analytical': True,
        }), content_type="application/json")
    data = response.json()

    assert response.status_code == 200
    assert 'tags' in data
    assert len(data['tags']) == 2

    assert 'wtm_analytical' in response.cookies
    assert response.cookies.get('wtm_analytical').value == 'true'

    response = client.post(
        '/wtm/lazy/', json.dumps({
            'analytical': False,
        }), content_type="application/json")
    data = response.json()

    assert response.status_code == 200
    assert 'tags' in data
    assert len(data['tags']) == 0

    assert 'wtm_analytical' in response.cookies
    assert response.cookies.get('wtm_analytical').value == 'false'


@pytest.mark.django_db
def test_traceable_lazy_cookies(client, site):
    tag_instant_traceable()
    tag_lazy_traceable()

    response = client.post(
        '/wtm/lazy/', json.dumps({
            'traceable': True,
        }), content_type="application/json")
    data = response.json()

    assert response.status_code == 200
    assert 'tags' in data
    assert len(data['tags']) == 2

    assert 'wtm_traceable' in response.cookies
    assert response.cookies.get('wtm_traceable').value == 'true'

    response = client.post(
        '/wtm/lazy/', json.dumps({
            'traceable': False,
        }), content_type="application/json")
    data = response.json()

    assert response.status_code == 200
    assert 'tags' in data
    assert len(data['tags']) == 0

    assert 'wtm_traceable' in response.cookies
    assert response.cookies.get('wtm_traceable').value == 'false'
