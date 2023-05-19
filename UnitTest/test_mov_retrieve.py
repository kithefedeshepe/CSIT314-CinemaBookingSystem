from rest_framework.test import APITestCase
from datetime import date
from core.models import Movie
import base64
from datetime import timedelta, date
from django.urls import reverse

class RetrieveMovieTestCase(APITestCase):
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
        self.movie1.save()
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
        self.movie2.save()

    def test_retrieve_movie(self):
        url = reverse('viewMov')  # URL for the search endpoint

        # Test case: Non-empty keyword
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        data = response.json()
        
        # Perform assertions on the response data
        self.assertIsInstance(data, list)  # Check if the response is a list
        self.assertEqual(len(data), 2)  
        print('\nUnit test retrieveMov passed')