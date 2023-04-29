from core.models import User
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase, APIClient
from rest_framework import status


class SuspendUserTestCase(APITestCase):
    def setUp(self):
        self.client = APIClient()
        # create an admin user
        self.admin_user = User.objects.create_user(username='admin', password='password', email='ad1@gmail.com', role='UserAdmin')
        self.admin_user.save()
        # log in the admin user
        response = self.client.post('/login/', {'username': 'admin', 'password': 'password'})
        self.admin_token = response.data['token']
        self.client.cookies['token'] = self.admin_token

    def test_suspend_user(self):
        # create a user to suspend
        user = User.objects.create_user(username='testuser', password='password', email='testusr@gmail.com', role='Customer')
        # suspend the user
        response = self.client.post('/suspendUser/', {'username': 'testuser'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # check that the user is suspended
        user.refresh_from_db()
        self.assertFalse(user.is_active)
        print("\nUnit test Suspend_1 passed")

    def test_suspension_nonexistent_user(self):
        self.usertest = User.objects.create_user(username='testuser', password='password', email='testusr@gmail.com', role='Customer')
        self.usertest.save()
        self.usertest1 = User.objects.create_user(username='testuser1', password='password', email='testusr1@gmail.com', role='Customer')
        self.usertest1.save()

        #login using not user admin
        response = self.client.post('/login/', {'username': 'testuser', 'password': 'password'})
        self.test_token = response.data['token']
        self.client.cookies['token'] = self.test_token

        response = self.client.post('/suspendUser/', {'username': 'testuser1'})
        # check that the user is suspended
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        print("\nUnit test Suspend_2 passed")
