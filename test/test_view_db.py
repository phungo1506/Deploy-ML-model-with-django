from django.test import TestCase

from django.urls import reverse

from django.contrib.auth.models import User

class URLTests(TestCase):
    """
    Test views in web.
    """
    def test_home(self):
        """
        Test view of url: localhost:8000/
        If response status code is 200 then pass test case.
        Else not pass.

        """
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
    def test_view(self):
        """
        Test view of url is name 'homepage'
        If response status code is 200 then pass test case.
        Else not pass.
        """
        url = reverse('homepage')
        response = self.client.get(url)
        assert response.status_code == 200

    def test_user_create(self):
        """
        Check database connection by creating a user.
        If user is creat then pass test case.
        Else not pass.

        """
        User.objects.create_user('phuoc', 'leminhphuoc@gmail.com', '123456')
        assert User.objects.count() == 1
