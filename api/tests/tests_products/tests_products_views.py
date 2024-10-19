from storeapp.models import Product
from api.tests.tests_products.base.test_base_product_views import TestBaseProductViews
from django.urls import reverse
from api.serializers import ProductSerializer

class TestProductsViews(TestBaseProductViews):
    def test_list_products(self):
        response = self.client.get(reverse('product-list'))
        serializer_product1 = ProductSerializer(Product.objects.get(id=self.product1.id))
        self.assertIn(serializer_product1.data, response.data)
        self.assertEqual(response.status_code, 200)
        
    def test_detail_product(self):
        response = self.client.get(reverse('product-detail', kwargs={'id': self.product1.id}))
        serializer_product1 = ProductSerializer(Product.objects.get(id=self.product1.id))
        self.assertEqual(serializer_product1.data, response.data)
        self.assertEqual(response.status_code, 200)
       
    def test_create_product(self):
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token_admin_user}')
        response = self.client.post(reverse('product-list'), self.data, format='json')
        product_exists = Product.objects.filter(name=self.data['name'], description=self.data['description']).exists()
        self.assertTrue(product_exists)
        self.assertEqual(response.status_code, 201)

    
    # TEST FIELD NAME
    def test_if_an_error_raises_when_trying_to_create_a_product_without_a_name(self):
        del self.data['name']
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token_admin_user}')
        response = self.client.post(reverse('product-list'), self.data, format='json')
        self.assertEqual(response.status_code, 400)
        
    def test_if_an_error_arises_when_trying_to_create_a_product_with_a_name_of_less_than_3_characters(self):
        self.data['name'] = 'dd' 
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token_admin_user}')
        response = self.client.post(reverse('product-list'), self.data, format='json')
        self.assertEqual(response.status_code, 400)
        
    def test_if_an_error_arises_when_trying_to_create_a_product_with_a_name_longer_than_200_characters(self):
        self.data['name'] = 'a' * 201
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token_admin_user}')
        response = self.client.post(reverse('product-list'), self.data, format='json')
        self.assertEqual(response.status_code, 400)
        
    def test_if_any_error_appears_when_trying_to_create_a_product_with_a_name_using_just_numbers(self):
        self.data['name'] = '1111'
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token_admin_user}')
        response = self.client.post(reverse('product-list'), self.data, format='json')
        self.assertEqual(response.status_code, 400)
        
    def test_if_any_error_appears_when_trying_to_create_a_product_with_an_empty_name(self):
        self.data['name'] = ''
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token_admin_user}')
        response = self.client.post(reverse('product-list'), self.data, format='json')
        self.assertEqual(response.status_code, 400)
    
    # TEST FIELD SLUG
    def test_if_an_error_raises_when_trying_to_create_a_product_without_a_slug(self):
        del self.data['slug']
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token_admin_user}')
        response = self.client.post(reverse('product-list'), self.data, format='json')
        self.assertEqual(response.status_code, 400)
            
    def test_if_an_error_arises_when_trying_to_create_a_product_with_a_slug_of_less_than_3_characters(self):
        self.data['slug'] = 'dd'
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token_admin_user}')
        response = self.client.post(reverse('product-list'), self.data, format='json')
        self.assertEqual(response.status_code, 400)
        
    def test_if_an_error_arises_when_trying_to_create_a_product_with_a_slug_longer_than_100_characters(self):
        self.data['slug'] = 'a' * 101
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token_admin_user}')
        response = self.client.post(reverse('product-list'), self.data, format='json')
        self.assertEqual(response.status_code, 400)
        
    def test_if_any_error_appears_when_trying_to_create_a_product_with_a_slug_using_just_numbers(self):
        self.data['slug'] = '1111'
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token_admin_user}')
        response = self.client.post(reverse('product-list'), self.data, format='json')
        self.assertEqual(response.status_code, 400)
        
    def test_if_any_error_appears_when_trying_to_create_a_product_with_an_empty_slug(self):
        self.data['slug'] = ''
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token_admin_user}')
        response = self.client.post(reverse('product-list'), self.data, format='json')
        self.assertEqual(response.status_code, 400)
        
    def test_if_an_error_raises_when_trying_to_create_a_product_without_a_inventory(self):
        del self.data['inventory']
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token_admin_user}')
        response = self.client.post(reverse('product-list'), self.data, format='json')
        self.assertEqual(response.status_code, 400)
        
    def test_if_an_error_raises_when_trying_to_create_a_product_without_a_old_price(self):
        del self.data['old_price']
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token_admin_user}')
        response = self.client.post(reverse('product-list'), self.data, format='json')
        self.assertEqual(response.status_code, 400)
    
    # TEST FIELD DESCRIPTION        
    def test_if_an_error_arises_when_trying_to_create_a_product_with_a_description_of_less_than_10_characters(self):
        self.data['description'] = 'd' * 9
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token_admin_user}')
        response = self.client.post(reverse('product-list'), self.data, format='json')
        self.assertEqual(response.status_code, 400)
        
    def test_if_an_error_arises_when_trying_to_create_a_product_with_a_description_longer_than_800_characters(self):
        self.data['description'] = 'a' * 801
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token_admin_user}')
        response = self.client.post(reverse('product-list'), self.data, format='json')
        self.assertEqual(response.status_code, 400)
        
    def test_if_any_error_appears_when_trying_to_create_a_product_with_a_description_using_just_numbers(self):
        self.data['description'] = '1111'
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token_admin_user}')
        response = self.client.post(reverse('product-list'), self.data, format='json')
        self.assertEqual(response.status_code, 400)
        
    def test_if_any_error_appears_when_trying_to_create_a_product_with_an_empty_description(self):
        self.data['description'] = ''
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token_admin_user}')
        response = self.client.post(reverse('product-list'), self.data, format='json')
        self.assertEqual(response.status_code, 400)
        
    def test_product_update(self):
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token_admin_user}')
        self.client.patch(reverse('product-detail', kwargs={'id': self.product1.id}), self.data)
        product = Product.objects.get(id=self.product1.id)
        
        self.assertEqual(product.name, self.data['name'])
        self.assertEqual(product.description, self.data['description'])
        self.assertEqual(product.discount, self.data['discount'])
        self.assertEqual(product.old_price, self.data['old_price'])
        self.assertEqual(product.slug, self.data['slug'])
        self.assertEqual(product.inventory, self.data['inventory'])
        self.assertEqual(product.top_deal, self.data['top_deal'])
        self.assertEqual(product.flash_sales, self.data['flash_sales'])
        
    def test_product_name_update(self):
        self.data = {'name': self.data['name']}
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token_admin_user}')
        self.client.patch(reverse('product-detail', kwargs={'id': self.product1.id}), self.data)
        product = Product.objects.get(id=self.product1.id)
        self.assertEqual(product.name, self.data['name'])
        
    def test_product_slug_update(self):
        self.data = {'slug': self.data['slug']}
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token_admin_user}')
        self.client.patch(reverse('product-detail', kwargs={'id': self.product1.id}), self.data)
        product = Product.objects.get(id=self.product1.id)
        self.assertEqual(product.slug, self.data['slug'])
        
    def test_product_inventory_update(self):
        self.data = {'inventory': self.data['inventory']}
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token_admin_user}')
        self.client.patch(reverse('product-detail', kwargs={'id': self.product1.id}), self.data)
        product = Product.objects.get(id=self.product1.id)
        self.assertEqual(product.inventory, self.data['inventory'])
                
    def test_delete_product(self):
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token_admin_user}')
        response = self.client.delete(reverse('product-detail', kwargs={'id': self.product1.id}))
        self.assertFalse(Product.objects.filter(id=self.product1.id).exists())
        self.assertEqual(response.status_code, 204)