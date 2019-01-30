import json

import pytest
from django.urls import reverse

from wagtail_tag_manager.views import CookieDeclarationIndexView
from wagtail_tag_manager.settings import TagTypeSettings
from wagtail_tag_manager.wagtail_hooks import CookieDeclarationModelAdmin


@pytest.mark.django_db
def test_manage_view(client):
    url = reverse("wtm:manage")

    response = client.get(url)
    assert response.status_code == 200

    response = client.post(url)
    assert response.status_code == 302


@pytest.mark.django_db
def test_state_view(client):
    url = reverse("wtm:state")

    response = client.get(url)
    assert response.status_code == 200
    assert json.loads(response.content) == {
        tag_type: config.get("value")
        for tag_type, config in TagTypeSettings.all().items()
    }


@pytest.mark.django_db
def test_variable_view(client, admin_user):
    url = reverse("wtm:variables")

    response = client.get(url)
    assert response.status_code == 404

    client.login(username="admin", password="password")
    response = client.get(url)
    assert response.status_code == 200


@pytest.mark.django_db
def test_cookie_declaration_index_view(client, admin_user):
    model_admin = CookieDeclarationModelAdmin()
    url = CookieDeclarationIndexView(model_admin=model_admin).index_url

    response = client.get(url)
    assert response.status_code == 302

    client.login(username="admin", password="password")
    response = client.post(url)
    assert response.status_code == 302
