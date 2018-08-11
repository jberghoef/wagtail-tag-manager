import pytest

from http.cookies import SimpleCookie

from tests.factories.tag import (
    tag_instant_functional, tag_instant_analytical, tag_instant_traceable,
    tag_lazy_traceable, tag_lazy_analytical, tag_lazy_functional)

from wagtail_tag_manager.models import Tag


@pytest.mark.django_db
def test_view(client, site):
    response = client.get('/')
    assert response.status_code == 200

    tag_instant_functional(tag_location=Tag.TOP_HEAD)
    client.cookies = SimpleCookie({'wtm_functional': 'true'})
    response = client.get('/')
    assert response.status_code == 200
    assert b'console.log("functional instant")' in response.content

    tag_instant_functional(tag_location=Tag.BOTTOM_HEAD)
    client.cookies = SimpleCookie({'wtm_functional': 'true'})
    response = client.get('/')
    assert response.status_code == 200
    assert b'console.log("functional instant")' in response.content

    tag_instant_analytical(tag_location=Tag.TOP_BODY)
    client.cookies = SimpleCookie({'wtm_analytical': 'true'})
    response = client.get('/')
    assert response.status_code == 200
    assert b'console.log("analytical instant")' in response.content

    tag_instant_traceable(tag_location=Tag.BOTTOM_BODY)
    client.cookies = SimpleCookie({'wtm_traceable': 'true'})
    response = client.get('/')
    assert response.status_code == 200
    assert b'console.log("traceable instant")' in response.content

    client.cookies = SimpleCookie({'wtm_functional': 'false'})
    response = client.get('/')
    assert response.status_code == 200
    assert b'console.log("functional instant")' in response.content
    assert b'console.log("analytical instant")' not in response.content
    assert b'console.log("traceable instant")' not in response.content
