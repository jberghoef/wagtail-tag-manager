import json
import pytest
from django.urls import reverse

from wagtail_tag_manager.models import TagTypeSettings


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
    assert json.loads(response.content) == TagTypeSettings.all()


@pytest.mark.django_db
def test_variable_view(client, user):
    url = reverse("wtm:variables")

    response = client.get(url)
    assert response.status_code == 404
