from core.models import User
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient
from api.checklist import *

class LoginTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.username = 'testuser'
        self.password = 'testpass'
        self.user = User.objects.create_user(username=self.username, password=self.password, email="test@gmail.com", role='Customer')

    #Login success
    def LogIn1(self):
        if not login_exists:
            return
        url = reverse('login')
        data = {'username': self.username, 'password': self.password}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        print("\nUnit test Login_1 passed")

    #Login fail
    def LogIn2(self):
        if not login_exists:
            return
        url = reverse('login')
        data = {'username': 'wronguser', 'password': self.password}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        print("\nUnit test Login_2 passed")

def tearDown(self):
    self.user.delete()