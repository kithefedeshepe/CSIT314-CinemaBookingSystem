from core.models import User
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from api.checklist import *
from django.urls import reverse
from datetime import timedelta, date
import base64

class TestAddFnb(APITestCase):

    def setUp(self):
        self.client = APIClient()
        # create an admin user
        self.admin_user = User.objects.create_user(username='admin', password='password', email='ad1@gmail.com', role='CinemaManager')
        self.admin_user.save()
        # log in the admin user
        response = self.client.post('/login/', {'username': 'admin', 'password': 'password'})
        self.admin_token = response.data['token']
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.admin_token)
        if add_fnb:
            self.url = reverse('addFnb')
        #setup movie img
        with open('UnitTest/testimg.png', 'rb') as f:
            img_data = f.read()
        self.base64_img_data = base64.b64encode(img_data).decode('utf-8')

    def test_add_fnb_success(self):
        if not add_fnb:
            return

        payload = {
            'menu': 'test',
            'menu_description': 'test',
            'price': 10.23,
            'menuIMG': self.base64_img_data 
        }

        response = self.client.post(self.url, payload)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        print("\nUnit test addFnb_1 passed")
        

    def test_add_fnb_unauthorized(self):
        if not add_fnb:
            return
        self.usertest = User.objects.create_user(username='testuser', password='password', email='testusr@gmail.com', role='Customer')
        self.usertest.save()
        response = self.client.post('/login/', {'username': 'testuser', 'password': 'password'})
        self.test_token = response.data['token']
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.test_token)

        payload = {
            'menu': 'test',
            'menu_description': 'test',
            'price': 10.23,
            'menuIMG': self.base64_img_data 
        }

        response = self.client.post(self.url, payload)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        print("\nUnit test addFnb_2 passed")

    def test_add_mov_invalid(self):
        if not add_mov:
            return

        payload = {
            'id': 'asdhfgasdhf71346715234thisdontmakeanysense',
        }

        response = self.client.post(self.url, payload)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        print("\nUnit test addFnb_3 passed")