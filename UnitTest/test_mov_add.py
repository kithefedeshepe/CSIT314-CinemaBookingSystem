from core.models import User, Movie
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from api.checklist import *
import base64
from django.urls import reverse
from datetime import timedelta, date

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
        #setup movie object
        self.movie_obj = Movie.objects.create(movie_title='test', genre='action', duration=timedelta(hours=1, minutes=30), release_date=date(2022, 5, 1), cast='John Doe',director='Jane Smith',movie_description='A test movie')

    def test_add_mov_success(self):
        if not add_mov:
            return

        payload = {
            'movie_title': 'test', 
            'genre': 'action',
            'duration' : timedelta(hours=1, minutes=30), 
            'release_date' :date(2022, 5, 1), 
            'cast' : 'John Doe',
            'director' :'Jane Smith',
            'movie_description' : 'A test movie'
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
            'release_date' :date(2022, 5, 1), 
            'cast' : 'John Doe',
            'director' :'Jane Smith',
            'movie_description' : 'A test movie'
        }
        response = self.client.post(self.url, payload)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        print("\nUnit test addMov_2 passed")

    def test_add_mov_invalid(self):
        if not add_mov:
            return

        payload = {
            'id': 'asdhfgasdhf71346715234thisdontmakeanysense',
        }

        response = self.client.post(self.url, payload)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        print("\nUnit test addMov_3 passed")