from core.models import User, Movie
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from api.checklist import *
from django.urls import reverse
from datetime import timedelta, date

class TestMovDel(APITestCase):
    def setUp(self):
        self.client = APIClient()
        # create an admin user
        self.admin_user = User.objects.create_user(username='admin', password='password', email='ad1@gmail.com', role='CinemaManager')
        self.admin_user.save()
        # log in the admin user
        response = self.client.post('/login/', {'username': 'admin', 'password': 'password'})
        self.admin_token = response.data['token']
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.admin_token)
        if del_mov:
            self.url = reverse('delMov')
        #setup movie object
        self.movie_obj = Movie.objects.create(movie_title='test', duration=timedelta(hours=1, minutes=30), release_date=date(2022, 5, 1), cast='John Doe',director='Jane Smith',movie_description='A test movie')


    def test_del_mov(self):
        if not del_mov:
            return
        
        self.movie_id = self.movie_obj.id
        payload = {
            'movie_title' : self.movie_obj.movie_title,
        }

        response = self.client.post(self.url, payload)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertFalse(Movie.objects.filter(id=self.movie_id).exists())
        print("\nUnit test delMov_1 passed")

    def test_delete_mov_no_permission(self):
        if not del_mov:
            return
        self.usertest = User.objects.create_user(username='testuser', password='password', email='testusr@gmail.com', role='Customer')
        self.usertest.save()

        response = self.client.post('/login/', {'username': 'testuser', 'password': 'password'})
        self.test_token = response.data['token']
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.test_token)

        self.movie_id = self.movie_obj.id
        payload = {
            'movie_title' : self.movie_obj.movie_title,
        }

        response = self.client.post(self.url, payload)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        print("\nUnit test delMov_2 passed")
    
    def test_del_mov_invalid(self):
        if not del_mov:
            return
        
        payload = {
            'id': '26134567134',
        }

        response = self.client.post(self.url, payload)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        print("\nUnit test delMov_3 passed")
