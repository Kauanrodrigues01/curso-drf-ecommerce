from django.test import TestCase
from rest_framework.test import APIClient
from django.urls import reverse

class TestBaseUserViews(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.data_user = {
            'email': 'test22@gmail.com',
            'first_name': 'John',
            'last_name': 'Fridey',
            'password': '#Password11',
            'password_confirmation': '#Password11'
        }
        
        self.url_register_user = reverse('user-register')
        return super().setUp()