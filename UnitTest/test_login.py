from core.models import User
from django.test import TestCase, skipIf
from django.urls import reverse
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient
from api.checklist import *

class LoginTest(TestCase):
    @skipIf(not login_exists, "Login API not implemented yet")
    def setUp(self):
        self.client = APIClient()
        self.username = 'testuser'
        self.password = 'testpass'
        self.user = User.objects.create_user(username=self.username, password=self.password, email="test@gmail.com", role='Customer')

    def test_login_with_correct_credentials(self):
        url = reverse('login')
        data = {'username': self.username, 'password': self.password}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_login_with_incorrect_username(self):
        url = reverse('login')
        data = {'username': 'wronguser', 'password': self.password}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

def tearDown(self):
    self.user.delete()