from core.models import User, CinemaRoom
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from api.checklist import *
from django.urls import reverse

class TestUpdateCinemaRoom(APITestCase):

    def setUp(self):
        self.client = APIClient()
        # create an admin user
        self.admin_user = User.objects.create_user(username='admin', password='password', email='ad1@gmail.com', role='CinemaManager')
        self.admin_user.save()
        # log in the admin user
        response = self.client.post('/login/', {'username': 'admin', 'password': 'password'})
        self.admin_token = response.data['token']
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.admin_token)
        if update_cinemaroom:
            self.url = reverse('updateCR') 
        # create cinemaroom
        self.cr_obj = CinemaRoom.objects.create(name='Sample', capacity=100)
        self.cr_obj.save()

    def test_update_CR_success(self):
        if not update_cinemaroom:
            return
        
        self.cr_update_target = 'Sample'
        payload = {
            'name': self.cr_update_target,
            'capacity': 50
        }

        response = self.client.post(self.url, payload)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(self.cr_obj.capacity, 50)
        print("\nUnit test updateCR_1 passed")


    def test_update_CR_unauthorized(self):
        if not update_cinemaroom:
            return
        self.usertest = User.objects.create_user(username='testuser', password='password', email='testusr@gmail.com', role='Customer')
        self.usertest.save()
        response = self.client.post('/login/', {'username': 'testuser', 'password': 'password'})
        self.test_token = response.data['token']
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.test_token)

        self.cr_update_target = 'Sample'
        payload = {
            'name': self.cr_update_target,
            'capacity': 50
        }


        response = self.client.post(self.url, payload)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(self.cr_obj.capacity, 100)
        print("\nUnit test updateCR_2 passed")
 

    def test_update_CR_notfound(self):
        if not update_cinemaroom:
            return
        
        self.cr_update_target = 'SampleNotFound'
        payload = {
            'name': self.cr_update_target,
            'capacity': 50
        }

        response = self.client.post(self.url, payload)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        print("\nUnit test updateCR_3 passed")
    
    def test_update_CR_invalid(self):
        if not update_cinemaroom:
            return
        
        self.cr_update_target = 'Sample'
        payload = {
            'name': self.cr_update_target,
            'capacity': -50
        }

        response = self.client.post(self.url, payload)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        print("\nUnit test updateCR_4 passed")