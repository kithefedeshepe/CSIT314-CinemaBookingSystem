from core.models import User, Movie, MovieSession, CinemaRoom
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from api.checklist import *
from django.urls import reverse
from datetime import timedelta, date

class TestDelMovSes(APITestCase):
    def setUp(self):
        self.client = APIClient()
        # create an admin user
        self.admin_user = User.objects.create_user(username='admin', password='password', email='ad1@gmail.com', role='CinemaManager')
        self.admin_user.save()
        # log in the admin user
        response = self.client.post('/login/', {'username': 'admin', 'password': 'password'})
        self.admin_token = response.data['token']
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.admin_token)
        if del_movses:
            self.url = reverse('delMS') 
        #setup movie object
        self.movie_obj = Movie.objects.create(movie_title='test', genre='action', duration=timedelta(hours=1, minutes=30), release_date=date(2022, 5, 1), cast='John Doe',director='Jane Smith',movie_description='A test movie')
        self.movie_obj.save()
        #setup cinema room
        self.cr_obj = CinemaRoom.objects.create(name='Sample', capacity=100)
        self.cr_obj.save()
        #setup movie session
        self.ms_obj = MovieSession.objects.create(movie=self.movie_obj, session_date=date(2022, 5, 25), cinema_room=self.cr_obj, session_time='19:30')
        self.ms_obj.save()

    def test_del_MS_success(self):
        if not del_movses:
            return
        
        self.ms_id = self.ms_obj.id
        payload = {
            'id': self.ms_id
        }

        response = self.client.post(self.url, payload)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertFalse(MovieSession.objects.filter(id=self.ms_id).exists())
        print("\nUnit test delMS_1 passed")


    def test_del_MS_unauthorized(self):
        if not del_movses:
            return
        self.usertest = User.objects.create_user(username='testuser', password='password', email='testusr@gmail.com', role='Customer')
        self.usertest.save()
        response = self.client.post('/login/', {'username': 'testuser', 'password': 'password'})
        self.test_token = response.data['token']
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.test_token)

        self.ms_id = self.ms_obj.id
        payload = {
            'id': self.ms_id
        }

        response = self.client.post(self.url, payload)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertTrue(MovieSession.objects.filter(id=self.ms_id).exists())
        print("\nUnit test delMS_2 passed")
