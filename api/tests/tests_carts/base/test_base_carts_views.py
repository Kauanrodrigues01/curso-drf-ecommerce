
from django.urls import reverse
from rest_framework.test import APIClient
from django.test import TestCase
from storeapp.models import Cart, Cartitems, Product
from core.models import User
from UserProfile.models import Customer


class TestBaseCartsViews(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.client = APIClient()
        cls.url_cart = reverse('cart')
        
        cls.user = User.objects.create_user(email='TesteUser@gmail.com', first_name='Teste', last_name='Teste', password='T#12345')
        cls.user_credentials = {
            'email': 'TesteUser@gmail.com',
            'password': 'T#12345'
        }
        cls.token_user = cls.client.post(reverse('login'), cls.user_credentials).data['access']
        return super().setUpTestData()
    
    def setUp(self):
        self.client = APIClient()
        return super().setUp()
    
    
class TestBaseCartsAndItemsViews(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.client = APIClient()
        cls.url_cart = reverse('cart')
        
        cls.user = User.objects.create_user(email='TesteUser@gmail.com', first_name='Teste', last_name='Teste', password='T#12345')
        cls.user_credentials = {
            'email': 'TesteUser@gmail.com',
            'password': 'T#12345'
        }
        cls.token_user = cls.client.post(reverse('login'), cls.user_credentials).data['access']
        
        cls.customer = Customer.objects.get(user=cls.user)
        
        # create cart
        cls.client.credentials(HTTP_AUTHORIZATION=f'Bearer {cls.token_user}')
        cls.client.post(cls.url_cart)
        cls.customer = Customer.objects.get(user=cls.user)
        cls.cart = Cart.objects.get(owner=cls.customer)
        
        # create products
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
        
        cls.cartitem_product2 = Cartitems.objects.create(
            cart=cls.cart,
            product=cls.product2,
            quantity=5
        )
        
        cls.cartitem_product3 = Cartitems.objects.create(
            cart=cls.cart,
            product=cls.product3,
            quantity=3
        )
        
        return super().setUpTestData()
    
    def setUp(self):
        self.client = APIClient()
        return super().setUp()