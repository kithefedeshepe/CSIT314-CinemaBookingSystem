from core.models import User, Movie
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from api.checklist import *
from django.urls import reverse
from datetime import timedelta, date
import base64

class TestAddMovie(APITestCase):

    def setUp(self):
        self.client = APIClient()
        # create an admin user
        self.admin_user = User.objects.create_user(username='admin', password='password', email='ad1@gmail.com', role='CinemaManager')
        self.admin_user.save()
        # log in the admin user
        response = self.client.post('/login/', {'username': 'admin', 'password': 'password'})
        self.admin_token = response.data['token']
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.admin_token)
        if add_mov:
            self.url = reverse('addMov')
        #setup movie img
        with open('UnitTest/testimg.png', 'rb') as f:
            img_data = f.read()
        self.base64_img_data = base64.b64encode(img_data).decode('utf-8')

    def test_add_mov_success(self):
        if not add_mov:
            return

        payload = {
            'movie_title': 'test', 
            'genre': 'action',
            'duration' : timedelta(hours=1, minutes=30), 
            'release_date' :'2022-5-1', 
            'cast' : 'John Doe',
            'director' :'Jane Smith',
            'movie_description' : 'A test movie',
            'posterIMG': self.base64_img_data,
            'featureIMG': self.base64_img_data
        }

        response = self.client.post(self.url, payload)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        print("\nUnit test addMov_1 passed")
        

    def test_add_mov_unauthorized(self):
        if not add_mov:
            return
        self.usertest = User.objects.create_user(username='testuser', password='password', email='testusr@gmail.com', role='Customer')
        self.usertest.save()
        response = self.client.post('/login/', {'username': 'testuser', 'password': 'password'})
        self.test_token = response.data['token']
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.test_token)

        payload = {
            'movie_title': 'test', 
            'genre': 'action',
            'duration' : timedelta(hours=1, minutes=30), 
            'release_date' :'2022-05-01', 
            'cast' : 'John Doe',
            'director' :'Jane Smith',
            'movie_description' : 'A test movie',
            'posterIMG': self.base64_img_data,
            'featureIMG': self.base64_img_data
        }
        response = self.client.post(self.url, payload)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        print("\nUnit test addMov_2 passed")
