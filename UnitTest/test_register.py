from core.models import User
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient
from api.checklist import *

class RegisterTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.username = 'testuser'
        self.password = 'testpass'
        self.email = 'testemail@gmail.com'

    def register_success(self):
        if not register_exists:
            return
        url = reverse('add')
        data = {'username': self.username, 'password': self.password, 'email': self.email}
        

    def register_fail(self):
        if not register_exists:
            return
        

    def tearDown(self):
        pass