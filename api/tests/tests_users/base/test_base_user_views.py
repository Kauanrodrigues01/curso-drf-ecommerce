from django.test import TestCase
import email
from rest_framework.test import APIClient
from django.urls import reverse
from core.models import User

class TestBaseUserViews(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.client = APIClient()
        cls.url_register_user = reverse('user-register')
        cls.data_user = {
            'email': 'test22@gmail.com',
            'first_name': 'John',
            'last_name': 'Fridey',
            'password': '#Password11',
            'password_confirmation': '#Password11'
        }
        
        cls.user_test = User.objects.create_user(email='TestUser@gmail.com', first_name='Robert', last_name='Garcia', password='#Test11')
        cls.user_test_credentials = {
            'email': cls.user_test.email,
            'password': '#Test11'
        }
        cls.token_user = cls.client.post(reverse('login'), cls.user_test_credentials).data['access']
        

    def setUp(self):
        self.client = APIClient()
