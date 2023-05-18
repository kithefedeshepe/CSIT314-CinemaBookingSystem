from rest_framework.test import APITestCase, APIClient
from rest_framework.authtoken.models import Token
from core.models import User


class LogoutViewTestCase(APITestCase):

    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='testuser', password='testpass', email='ngutestuser@gmail.com', role='Customer')
        self.token = Token.objects.create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)

    def test_authentication(self):
        response = self.client.post('/logout/')
        self.assertEqual(response.status_code, 200)
        print("\nUnit test Logout_1 passed")

    def test_logout_not_authenticated(self):
        self.client.force_authenticate(user=None)
        response = self.client.post('/logout/')
        self.assertEqual(response.status_code, 403)
        print("\nUnit test Logout_2 passed")
