import django.urls
from rest_framework.test import APIClient
from django.test import TestCase
from storeapp.models import Category
from core.models import User
from django.urls import reverse

class TestBaseCategoryViews(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.client = APIClient()
        
        cls.category1 = Category.objects.create(
            title='Category test 1',
            slug='category-test-1',
            icon='icon1.png'
        )

        cls.category2 = Category.objects.create(
            title='Category test 2',
            slug='category-test-2',
            icon='icon2.png'
        )

        cls.category3 = Category.objects.create(
            title='Category test 3',
            slug='category-test-3',
            icon='icon3.png'
        )
        
        cls.data =  {
            'title': 'Category test',
            'slug': 'category-test',
            'icon': 'icon4.png'
        }
        
        cls.admin_user = User.objects.create_superuser(email='AdminUserTeste@gmail.com', first_name='John', last_name='Murphy', password='$Teste123')
        
        cls.credentials_admin_user = {
            'email': 'AdminUserTeste@gmail.com', 
            'password': '$Teste123'
        }
        
        cls.token_admin_user = cls.client.post(reverse('login'), cls.credentials_admin_user).data['access']
    
    def setUp(self):
        self.client = APIClient()