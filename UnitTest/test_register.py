from django.test import TestCase
from rest_framework.test import APIClient
from django.contrib.auth.hashers import check_password
from django.urls import reverse
from rest_framework import status
from api.checklist import *
from core.models import User

class RegisterAccountTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.url = reverse('add')

    def test_Register1(self):
        if not register_exists:
            return
        payload = {
            'username': 'testuser',
            'email': 'testuser@example.com',
            'password': 'testpassword'
        }
        response = self.client.post(self.url, payload, format='json')

        # Check if response is 200
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Check if user was created successfully
        user_exists = User.objects.filter(username=payload['username']).exists()
        self.assertTrue(user_exists)

        # Check if password was encrypted
        user = User.objects.get(username=payload['username'])
        self.assertTrue(check_password(payload['password'], user.password))
        print("\nUnit test Register_1 passed")
