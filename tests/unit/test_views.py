import pytest
from django.urls import reverse


@pytest.mark.django_db
def test_manage_view(client):
    url = reverse('wtm:manage')

    response = client.get(url)
    assert response.status_code == 200

    response = client.post(url)
    assert response.status_code == 302
