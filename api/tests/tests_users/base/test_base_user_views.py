from django.test import TestCase
from rest_framework.test import APIClient


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
        return super().setUp()