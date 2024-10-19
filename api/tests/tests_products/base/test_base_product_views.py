from django.test import TestCase
from storeapp.models import Product
from rest_framework.test import APIClient
from django.urls import reverse
from core.models import User

class TestBaseProductViews(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.client = APIClient()  # Inicialize o cliente aqui

        # Crie os produtos
        cls.product1 = Product.objects.create(
            name='Produto teste 1',
            description='Descrição teste 1',
            discount=True,
            old_price=200.00,
            slug='produto-teste-1',
            inventory=10,
            top_deal=True,
            flash_sales=False
        )
        
        cls.product2 = Product.objects.create(
            name='Produto teste 2',
            description='Descrição teste 2',
            discount=False,
            old_price=150.00,
            slug='produto-teste-2',
            inventory=15,
            top_deal=False,
            flash_sales=True
        )
        
        cls.product3 = Product.objects.create(
            name='Produto teste 3',
            description='Descrição teste 3',
            discount=True,
            old_price=300.00,
            slug='produto-teste-3',
            inventory=8,
            top_deal=False,
            flash_sales=False
        )
        
        cls.data = {
            'name': 'New Product',
            'description': 'New description',
            'discount': False,
            'old_price': 250.00,
            'slug': 'new-product',
            'inventory': 20,
            'top_deal': False,
            'flash_sales': True
        }
        
        # Admin User
        cls.admin_user = User.objects.create_superuser(email='AdminUserTest@gmail.com', first_name='John', last_name='Murphy', password='$Teste123')
        cls.credentials_admin_user = {
            'email': 'AdminUserTest@gmail.com', 
            'password': '$Teste123'
        }
        cls.token_admin_user = cls.client.post(reverse('login'), cls.credentials_admin_user).data['access']
        
        # Common User
        cls.common_user = User.objects.create_user(email='CommonUserTest@gmail.com', first_name='John', last_name='Murphy', password='$Teste123')
        cls.credentials_common_user = {
            'email': 'CommonUserTest@gmail.com', 
            'password': '$Teste123'
        }
        cls.token_common_user = cls.client.post(reverse('login'), cls.credentials_common_user).data['access']

    def setUp(self):
        self.client = APIClient() 