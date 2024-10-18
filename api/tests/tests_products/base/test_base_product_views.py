from django.test import TestCase
from storeapp.models import Product
from rest_framework.test import APIClient
from django.urls import reverse

class TestBaseProductViews(TestCase):
    def setUp(self):
        self.client = APIClient()
        
        self.product1 = Product.objects.create(
            name='Produto teste 1',
            description='Descrição teste 1',
            discount=True,
            old_price=200.00,
            slug='produto-teste-1',
            inventory=10,
            top_deal=True,
            flash_sales=False
        )
        
        self.product2 = Product.objects.create(
            name='Produto teste 2',
            description='Descrição teste 2',
            discount=False,
            old_price=150.00,
            slug='produto-teste-2',
            inventory=15,
            top_deal=False,
            flash_sales=True
        )
        
        self.product3 = Product.objects.create(
            name='Produto teste 3',
            description='Descrição teste 3',
            discount=True,
            old_price=300.00,
            slug='produto-teste-3',
            inventory=8,
            top_deal=False,
            flash_sales=False
        )
        
        self.data = {
            'name': 'New Product',
            'description': 'New description',
            'discount': False,
            'old_price': 250.00,
            'slug': 'new-product',
            'inventory': 20,
            'top_deal': False,
            'flash_sales': True
        }
        return super().setUp()