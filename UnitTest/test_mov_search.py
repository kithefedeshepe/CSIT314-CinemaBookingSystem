from rest_framework.test import APITestCase
from datetime import date
from core.models import Movie
import base64
from datetime import timedelta, date
from django.urls import reverse

class SearchMovieTestCase(APITestCase):
    def setUp(self):
        with open('UnitTest/testimg.png', 'rb') as f:
            img_data = f.read()
        self.base64_img_data = base64.b64encode(img_data).decode('utf-8')
        # Create test data
        self.movie1 = Movie.objects.create(
            movie_title='Movie 1',
            genre='Action',
            duration=timedelta(hours=1, minutes=30),
            release_date='2022-1-1',
            cast='Actor 1, Actress 1',
            director='Director 1',
            movie_description='Description 1',
            posterIMG=self.base64_img_data,
            featureIMG=self.base64_img_data
        )

        self.movie2 = Movie.objects.create(
            movie_title='Movie 2',
            genre='Comedy',
            duration=timedelta(hours=1, minutes=30),
            release_date='2022-1-1',
            cast='Actor 2, Actress 2',
            director='Director 2',
            movie_description='Description 2',
            posterIMG=self.base64_img_data,
            featureIMG=self.base64_img_data
        )
        

    def test_search_movie_empty_keyword(self):
        url = reverse('searchProfile')  # URL for the search endpoint

        # Test case: Empty keyword
        response = self.client.post(url, data={})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {'error': 'Please provide a keyword to search for'})
        print('\nUnit test searchMov_1 passed')

    def test_search_movie_matching_keyword(self):
        url = reverse('searchProfile')  # URL for the search endpoint

        # Test case: Non-empty keyword
        keyword = 'Action'
        response = self.client.post(url, data={'keyword': keyword})
        self.assertEqual(response.status_code, 200)
        data = response.json()
        # Perform assertions on the response data
        self.assertIsInstance(data, list)  # Check if the response is a list
        self.assertEqual(len(data), 1)  # Check if there is one movie in the response
        movie = data[0]
        self.assertEqual(movie['movie_title'], self.movie1.movie_title)  # Check movie title
        self.assertEqual(movie['genre'], self.movie1.genre)  # Check genre
        # Perform assertions for the remaining fields if needed
        print('\nUnit test searchMov_2 passed')

    def test_search_movie_non_existing_keyword(self):
        url = reverse('searchProfile')  # URL for the search endpoint

        # Test case: Non-existing keyword
        keyword = 'Drama'
        response = self.client.post(url, data={'keyword': keyword})
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIsInstance(data, list)  # Check if the response is a list
        self.assertEqual(len(data), 0)  # Check if there are no movies in the response
        print('\nUnit test searchMov_3 passed')
