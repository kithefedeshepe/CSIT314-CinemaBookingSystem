from django.test import TestCase, Client
from django.urls import reverse
from core.models import User, MovieImage
import json

class TestDeleteMovieImage(TestCase):

    def setUp(self):
        self.client = Client()
        self.manager_user = User.objects.create_user(username='testuser', password='12345')
        self.manager_user.user_type = 'cinemaManager'
        self.manager_user.save()

        self.movie_image = MovieImage.objects.create(image='image_path.jpg')
        self.url = reverse('delete_image', args=[self.movie_image.id])

    def test_delete_image_success(self):
        self.client.login(username='testuser', password='12345')
        response = self.client.delete(self.url)
        self.assertEqual(response.status_code, 204)
        self.assertFalse(MovieImage.objects.filter(id=self.movie_image.id).exists())

    def test_delete_image_unauthorized(self):
        response = self.client.delete(self.url)
        self.assertEqual(response.status_code, 403)

    def test_delete_image_not_found(self):
        self.client.login(username='testuser', password='12345')
        url = reverse('delete_image', args=[999])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, 404)

    def test_delete_image_unknown_exception(self):
        self.client.login(username='testuser', password='12345')
        with patch('myapp.views.MovieImage.objects.filter') as mock_filter:
            mock_filter.side_effect = Exception("unknown exception")
            response = self.client.delete(self.url)
        self.assertEqual(response.status_code, 500)
