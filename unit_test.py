import django.test import TestCase
import django.urls import reverse
from .models import User

class TestLogin(TestCase):
    def test_login_success(self):
        username = "test_user"
        password = "test_password"
        
        response = requests.post("https://csit-314-cinema-booking-system.vercel.app/login", json={"username": username, "password": password})
        
        self.assertEqual(response.status_code, 200)

    def test_login_failure(self):
        username = "test_user"
        password = "wrong_password"
        
        response = requests.post("https://csit-314-cinema-booking-system.vercel.app/login", json={"username": username, "password": password})
 
        self.assertEqual(response.status_code, 400)