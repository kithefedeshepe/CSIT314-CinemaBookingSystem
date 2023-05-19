from rest_framework.test import APITestCase
from rest_framework.authtoken.models import Token
from rest_framework import status
from django.urls import reverse
from core.models import CinemaRoom, User

class RetrieveCinemaRoomTestCase(APITestCase):
    def setUp(self):
        # Create a user and authenticate
        self.user = User.objects.create_user(username='testuser', password='testpassword', email='nguconhaysua@gmail.com', role='CinemaManager')
        self.token = Token.objects.create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)

    def test_retrieve_cr_authorized(self):
        url = reverse('viewAllCR')  # Assuming you have defined the URL pattern for searchCR view
        keyword = 'Cinema Room 1'

        # Create some test CinemaRoom instances with matching keyword
        cinema_room1 = CinemaRoom.objects.create(name='Cinema Room 1', capacity=100)
        cinema_room2 = CinemaRoom.objects.create(name='Cinema Room 2', capacity=200)

        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)  # Assert that 2 cinema rooms are returned

        # Assert the response data for each cinema room
        self.assertEqual(response.data[0]['id'], cinema_room1.id)
        self.assertEqual(response.data[0]['name'], cinema_room1.name)
        self.assertEqual(response.data[0]['capacity'], cinema_room1.capacity)

        self.assertEqual(response.data[1]['id'], cinema_room2.id)
        self.assertEqual(response.data[1]['name'], cinema_room2.name)
        self.assertEqual(response.data[1]['capacity'], cinema_room2.capacity)
        print('\nUnit test retrieveCR_1 passed')

    def test_retrieve_cr_unauthorized(self):
        url = reverse('viewAllCR')  # Assuming you have defined the URL pattern for searchCR view
        self.usertest = User.objects.create_user(username='testuser123', password='password', email='testusr@gmail.com', role='Customer')
        self.usertest.save()

        response = self.client.post('/login/', {'username': 'testuser123', 'password': 'password'})
        self.test_token = response.data['token']
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.test_token)
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        print('\nUnit test retrieveCR_1 passed')
