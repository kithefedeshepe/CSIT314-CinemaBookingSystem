from rest_framework.test import APITestCase
from rest_framework.authtoken.models import Token
from rest_framework import status
from django.urls import reverse
from core.models import CinemaRoom, User

class SearchCinemaRoomTestCase(APITestCase):
    def setUp(self):
        # Create a user and authenticate
        self.user = User.objects.create_user(username='testuser', password='testpassword', email='nguconhaysua@gmail.com', role='CinemaManager')
        self.token = Token.objects.create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)

    def test_search_cinema_room_with_keyword(self):
        url = reverse('searchCR')  # Assuming you have defined the URL pattern for searchCR view
        keyword = 'Cinema Room 1'

        # Create some test CinemaRoom instances with matching keyword
        cinema_room1 = CinemaRoom.objects.create(name='Cinema Room 1', capacity=100)
        cinema_room2 = CinemaRoom.objects.create(name='Cinema Room 2', capacity=200)

        response = self.client.post(url, {'keyword': keyword})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)  # Assert that 2 cinema rooms are returned

        # Assert the response data for each cinema room
        self.assertEqual(response.data[0]['id'], cinema_room1.id)
        self.assertEqual(response.data[0]['name'], cinema_room1.name)
        self.assertEqual(response.data[0]['capacity'], cinema_room1.capacity)
        print('\nUnit test searchCR_1 passed')

    def test_search_cinema_room_without_keyword(self):
        url = reverse('searchCR')  # Assuming you have defined the URL pattern for searchCR view

        response = self.client.post(url)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        print('\nUnit test searchCR_2 passed')
