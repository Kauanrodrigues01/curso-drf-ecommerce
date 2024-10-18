from django.test import TestCase
from rest_framework.test import APIClient
from UserProfile.models import Customer
from core.models import User


class TestBaseUserViews(TestCase):
    def setUp(self):
        self.client = APIClient()
        
        return super().setUp()