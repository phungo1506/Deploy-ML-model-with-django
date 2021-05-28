from django.test import TestCase

from django.urls import reverse

from django.contrib.auth.models import User

class URLTests(TestCase):
    def test_home(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
    def test_view(self):
        url = reverse('homepage')
        response = self.client.get(url)
        assert response.status_code == 200

    def test_user_create(self):
        User.objects.create_user('john', 'lennon@thebeatles.com', 'johnpassword')
        assert User.objects.count() == 1
