import pytest
from django.urls import reverse
from database.models import Model_predict

def func(x):
    return x+5
def test():
    assert func(4) == 9




from django.contrib.auth.models import User


@pytest.mark.django_db
def test_user_create():
  User.objects.create_user('john', 'lennon@thebeatles.com', 'johnpassword')
  assert User.objects.count() == 1

import pytest

from django.urls import reverse

@pytest.mark.django_db
def test_view(client):
   url = reverse('homepage')
   response = client.get(url)
   assert response.status_code == 200
# @pytest.mark.django_db
# def test_unauthorized(client):
#    url = reverse('predictImage')
#    response = client.get(url)
#    assert response.status_code == 401
#
#
# @pytest.mark.django_db
# def test_superuser_view(admin_client):
#    url = reverse('admin')
#    response = admin_client.get(url)
#    assert response.status_code == 200