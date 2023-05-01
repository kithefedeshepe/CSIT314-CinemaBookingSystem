from core.models import User
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from api.checklist import *

class ReactivateUserTestCase(APITestCase):
    def setUp(self):
        self.client = APIClient()
        # create an admin user
        self.admin_user = User.objects.create_user(username='admin', password='password', email='ad1@gmail.com', role='UserAdmin')
        self.admin_user.save()
        # log in the admin user
        response = self.client.post('/login/', {'username': 'admin', 'password': 'password'})
        self.admin_token = response.data['token']
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.admin_token)

    def test_reactivate_user(self):
        if not reactive_exists:
            return
        # create a user to suspend
        user = User.objects.create_user(username='testuser', password='password', email='testusr@gmail.com', role='Customer')
        # suspend the user
        response = self.client.post('/suspendUser/', {'username': 'testuser'})
        # reactivate
        response = self.client.post('/reactivateUser/', {'username': 'testuser'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # check that the user is suspended
        user.refresh_from_db()
        self.assertTrue(user.is_active)
        print("\nUnit test Reactivate_1 passed")

    def test_reactivate_no_permission(self):
        if not reactive_exists:
            return
        #create test data
        self.usertest = User.objects.create_user(username='testuser', password='password', email='testusr@gmail.com', role='Customer')
        self.usertest.save()
        self.usertest1 = User.objects.create_user(username='testuser1', password='password', email='testusr1@gmail.com', role='Customer')
        self.usertest1.save()

        # suspend the user
        response = self.client.post('/suspendUser/', {'username': 'testuser1'})
        #login using not user admin
        response = self.client.post('/login/', {'username': 'testuser', 'password': 'password'})
        self.test_token = response.data['token']
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.test_token)

        # reactivate
        response = self.client.post('/reactivateUser/', {'username': 'testuser1'})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        # check that the user is suspended
        print("\nUnit test Reactivate_2 passed")
    
    def test_reactivate_nonexist_user(self):
        if not reactive_exists:
            return
        # reactivate
        response = self.client.post('/reactivateUser/', {'username': 'dhjfasjgh'})
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        # check that the user is suspended
        print("\nUnit test Reactivate_3 passed")