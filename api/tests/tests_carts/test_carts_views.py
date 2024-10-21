from api.tests.tests_carts.base.test_base_carts_views import TestBaseCartsViews, TestBaseCartsAndItemsViews
from django.urls import reverse
from storeapp.models import Cart, Cartitems
from UserProfile.models import Customer
from api.serializers import CartitemsSerializer
from storeapp.views import cart

class TestCartsViews(TestBaseCartsViews):
    def test_create_a_card(self):
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token_user}')
        response = self.client.post(self.url_cart)
        customer = Customer.objects.get(user=self.user)
        self.assertTrue(Cart.objects.filter(owner=customer).exists())
        self.assertEqual(response.status_code, 201)
        
    def test_whether_an_error_appears_when_trying_to_create_a_cart_if_there_is_already_a_cart_created(self):
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token_user}')
        response = self.client.post(self.url_cart)
        self.assertEqual(response.status_code, 201)
        
        response = self.client.post(self.url_cart)
        customer = Customer.objects.get(user=self.user)
        carts = Cart.objects.filter(owner=customer)
        self.assertEqual(len(carts), 1)
        self.assertEqual(response.status_code, 400)
        
    def test_if_an_error_arises_when_trying_to_list_the_items_in_the_cart_without_the_cart_being_created(self):
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token_user}')
        response = self.client.get(reverse('cartitems-list'))
        self.assertEqual(response.status_code, 404)
        
    # TEST PERMISSIONS
    def test_if_an_unauthenticated_user_cannot_create_a_cart(self):
        response = self.client.post(self.url_cart)
        self.assertEqual(response.status_code, 401)
    
    def test_whether_an_unauthenticated_user_cannot_access_the_cart_details_route(self):
        response = self.client.get(reverse('cartitems-list'))
        self.assertEqual(response.status_code, 401)
        
class TestCartsAndItemsViews(TestBaseCartsAndItemsViews):
    # TEST LIST ITEMS
    def test_list_products_from_cart(self):
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token_user}')
        response = self.client.get(reverse('cartitems-list'))
        
        serializer_cartitem_product2 = CartitemsSerializer(self.cartitem_product2)
        serializer_cartitem_product3 = CartitemsSerializer(self.cartitem_product3)
        
        self.assertIn(serializer_cartitem_product2.data, response.data)
        self.assertIn(serializer_cartitem_product3.data, response.data)
        self.assertEqual(response.status_code, 200)
    
    # TEST ADD ITEMS
    def test_add_products_to_cart(self):
        data = {
            'product': self.product1.id,
            'quantity': 3
        }
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token_user}')
        response = self.client.post(reverse('cartitems-list'), data=data)
        
        cartitem_exists = Cartitems.objects.filter(cart=self.cart, product=self.product1, quantity=data['quantity']).exists()
        self.assertTrue(cartitem_exists)
        self.assertEqual(response.status_code, 201)
        
    def test_if_an_error_arises_when_trying_to_add_an_item_to_the_cart_without_a_product(self):
        data = {
            'quantity': 3
        }
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token_user}')
        response = self.client.post(reverse('cartitems-list'), data=data)
        self.assertEqual(response.status_code, 400)
        
    def test_if_an_error_arises_when_adding_a_product_to_the_cart_with_an_invalid_pk(self):
        data = {
            'product': f'{self.product1.id}2',
            'quantity': 3
        }
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token_user}')
        response = self.client.post(reverse('cartitems-list'), data=data)
        self.assertEqual(response.status_code, 400)
        
    def test_whether_quantity_is_considered_1_when_it_is_not_informed(self):
        data = {'product': self.product1.id}
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token_user}')
        response = self.client.post(reverse('cartitems-list'), data=data)
        
        cartitem_exists = Cartitems.objects.filter(cart=self.cart, product=self.product1).exists()
        cartitem = Cartitems.objects.get(cart=self.cart, product=self.product1)
        self.assertTrue(cartitem_exists)
        self.assertEqual(cartitem.quantity, 1)
        self.assertEqual(response.status_code, 201)
        
    def test_if_an_error_arises_when_trying_to_add_a_product_with_negative_quantity(self):
        data = {
            'product': self.product1.id,
            'quantity': -1
        }
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token_user}')
        response = self.client.post(reverse('cartitems-list'), data=data)
        
        cartitem_exists = Cartitems.objects.filter(cart=self.cart, product=self.product1, quantity=data['quantity']).exists()
        self.assertFalse(cartitem_exists)
        self.assertEqual(response.status_code, 400)
        
    def test_whether_to_add_quantity_to_the_cart_item_if_it_already_exists(self):
        data = {
            'product': self.product2.id,
            'quantity': 1
        }
        old_quantity = self.cartitem_product2.quantity
        
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token_user}')
        response = self.client.post(reverse('cartitems-list'), data=data)
        
        self.cartitem_product2.refresh_from_db()
        new_quantity = self.cartitem_product2.quantity

        expected_quantity = old_quantity + data['quantity']
        cartitem_exists = Cartitems.objects.filter(cart=self.cart, product=self.product2, quantity=new_quantity).exists()
        
        self.assertTrue(cartitem_exists)
        self.assertEqual(self.cartitem_product2.quantity, expected_quantity)
        self.assertEqual(response.status_code, 201) 
        
    def test_if_an_error_arises_when_trying_to_add_a_quantity_of_product_that_is_not_in_inventory(self):
        data = {
            'product': self.product1.id,
            'quantity': (self.product1.inventory + 2)
        }
        
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token_user}')
        response = self.client.post(reverse('cartitems-list'), data=data)

        cartitem_exists = Cartitems.objects.filter(cart=self.cart, product=self.product2, quantity=data['quantity']).exists()
        self.assertFalse(cartitem_exists)
        self.assertEqual(response.status_code, 400)
        
    def test_prevent_adding_quantity_exceeding_inventory_for_existing_cart_item(self):
        data = {
            'product': self.product2.id,
            'quantity': 11
        }
        
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token_user}')
        response = self.client.post(reverse('cartitems-list'), data=data)

        cartitem_exists = Cartitems.objects.filter(cart=self.cart, product=self.product2, quantity=data['quantity']).exists()
        self.assertFalse(cartitem_exists)
        self.assertEqual(response.status_code, 400)
  
    # TEST UPDATE QUANTITY
    def test_updating_the_quantity_of_a_product_in_the_cart(self):
        data = {
            'quantity': 1
        }
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token_user}')
        response = self.client.patch(reverse('cartitems-detail', kwargs={'id': self.cartitem_product2.id}), data=data)
        
        self.cartitem_product2.refresh_from_db()
        self.assertEqual(self.cartitem_product2.quantity, 1)
        self.assertEqual(response.status_code, 200)
        
    def test_if_an_error_arises_when_trying_to_update_a_cart_item_that_does_not_exist(self):
        data = {
            'quantity': 1
        }
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token_user}')
        response = self.client.patch(reverse('cartitems-detail', kwargs={'id': 99}), data=data)
        self.assertEqual(response.status_code, 404)
    
    # TEST DELETE 
    def test_deleting_a_product_from_the_cart(self):
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token_user}')
        response = self.client.delete(reverse('cartitems-detail', kwargs={'id': self.cartitem_product2.id}))
        
        cartitem_product2_exists = Cartitems.objects.filter(cart=self.cart, product=self.product2).exists()
        
        self.assertFalse(cartitem_product2_exists)
        self.assertEqual(response.status_code, 204)
        
    # TEST PERMISSIONS
    def test_whether_an_unauthenticated_user_cannot_access_the_list_cart_items_route(self):
        response = self.client.get(reverse('cartitems-list'))
        self.assertEqual(response.status_code, 401)
        
    def test_whether_an_unauthenticated_user_cannot_access_the_add_cart_items_route(self):
        data = {
            'product': self.product1.id,
            'quantity': 3
        }
        response = self.client.post(reverse('cartitems-list'), data=data)
        
        cartitem_exists = Cartitems.objects.filter(cart=self.cart, product=self.product1, quantity=data['quantity']).exists()
        self.assertFalse(cartitem_exists)
        self.assertEqual(response.status_code, 401)
        
    def test_whether_an_unauthenticated_user_cannot_access_the_cart_item_update_route(self):
        data = {
            'quantity': 1
        }
        response = self.client.patch(reverse('cartitems-detail', kwargs={'id': self.cartitem_product2.id}), data=data)
        self.assertEqual(response.status_code, 401)
        
    def test_whether_an_unauthenticated_user_cannot_access_the_route_to_delete_items_from_the_cart(self):
        response = self.client.delete(reverse('cartitems-detail', kwargs={'id': self.cartitem_product2.id}))
        self.assertEqual(response.status_code, 401)