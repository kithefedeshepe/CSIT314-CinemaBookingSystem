from core.models import User
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from api.checklist import *
import base64
from django.urls import reverse

class MovieImageAddTestCase(APITestCase):
    def setUp(self):
        self.client = APIClient()
        # create an admin user
        self.admin_user = User.objects.create_user(username='admin', password='password', email='ad1@gmail.com', role='CinemaManager')
        self.admin_user.save()
        # log in the admin user
        response = self.client.post('/login/', {'username': 'admin', 'password': 'password'})
        self.admin_token = response.data['token']
        self.client.cookies['token'] = self.admin_token
        if add_mov_img:
            self.url = reverse('addImg')
        with open('UnitTest/testimg.png', 'rb') as f:
            img_data = f.read()
        self.base64_img_data = base64.b64encode(img_data).decode('utf-8')


    def test_add_movimg(self):
        if not add_mov_img:
            return
        payload = {
            'movie_id': '0',
            'img_data': self.base64_img_data
        }

        response = self.client.post('/addImg/', payload)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        print("\nUnit test addImg_1 passed")

    def test_add_movimg_no_permission(self):
        if not add_mov_img:
            return
        self.usertest = User.objects.create_user(username='testuser', password='password', email='testusr@gmail.com', role='Customer')
        self.usertest.save()

        response = self.client.post('/login/', {'username': 'testuser', 'password': 'password'})
        self.test_token = response.data['token']
        self.client.cookies['token'] = self.test_token

        payload = {
            'movie_id': '0',
            'img_data': self.base64_img_data
        }

        response = self.client.post(self.url, payload)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        print("\nUnit test addImg_2 passed")


    
    def test_add_movimg_id_notfound(self):
        if not add_mov_img:
            return
        
        payload = {
            'movie_id': '190234781239412736412',
            'img_data': self.base64_img_data
        }

        response = self.client.post(self.url, payload)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        print("\nUnit test addImg_3 passed")
    
    def test_add_movimg_invalid(self):
        if not add_mov_img:
            return
        
        payload = {
            'img_data': self.base64_img_data
        }

        response = self.client.post(self.url, payload)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        print("\nUnit test addImg_4 passed")
