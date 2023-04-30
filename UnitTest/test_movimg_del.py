from core.models import User, MovieImage, Movie
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from api.checklist import *
import base64
from django.urls import reverse
from datetime import timedelta, date

class TestDeleteMovieImage(APITestCase):

    def setUp(self):
        self.client = APIClient()
        # create an admin user
        self.admin_user = User.objects.create_user(username='admin', password='password', email='ad1@gmail.com', role='CinemaManager')
        self.admin_user.save()
        # log in the admin user
        response = self.client.post('/login/', {'username': 'admin', 'password': 'password'})
        self.admin_token = response.data['token']
        self.client.cookies['token'] = self.admin_token

        #setup image
        if del_mov_img:
            self.url = reverse('delImg')

        with open('UnitTest/testimg.png', 'rb') as f:
            img_data = f.read()
        self.base64_img_data = base64.b64encode(img_data).decode('utf-8')

        #setup movie object
        self.movie_obj = Movie.objects.create(id = 0, movie_title='test', duration=timedelta(hours=1, minutes=30), release_date=date(2022, 5, 1), cast='John Doe',director='Jane Smith',movie_description='A test movie')
        
        #setup movie image object
        self.movie_image = MovieImage.objects.create(movie=self.movie_obj, data=self.base64_img_data)

    def test_delete_image_success(self):
        if not del_mov_img:
            return
        image_uuid = self.movie_image.id
        payload = {
            'id': image_uuid,
        }

        response = self.client.post(self.url, payload)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertFalse(MovieImage.objects.filter(id=image_uuid).exists())
        print("\nUnit test delImg_1 passed")
        

    def test_delete_image_unauthorized(self):
        if not del_mov_img:
            return
        self.usertest = User.objects.create_user(username='testuser', password='password', email='testusr@gmail.com', role='Customer')
        self.usertest.save()
        response = self.client.post('/login/', {'username': 'testuser', 'password': 'password'})
        self.test_token = response.data['token']
        self.client.cookies['token'] = self.test_token

        image_uuid = self.movie_image.id
        payload = {
            'id': image_uuid,
        }

        response = self.client.post(self.url, payload)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertTrue(MovieImage.objects.filter(id=image_uuid).exists())
        print("\nUnit test delImg_2 passed")

    def test_delete_image_not_found(self):
        if not del_mov_img:
            return
        image_uuid = self.movie_image.id
        payload = {
            'id': 'asdhfgasdhf71346715234thisdontmakeanysense',
        }

        response = self.client.post(self.url, payload)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        print("\nUnit test delImg_3 passed")

