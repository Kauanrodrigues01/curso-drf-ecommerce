from UserProfile.models import Customer
from core.models import User
from api.tests.tests_users.base.test_base_user_views import TestBaseUserViews
from django.urls import reverse
from api.serializers import UserSerializer

class TestUserViews(TestBaseUserViews):
    def test_if_the_user_me_route_returns_the_logged_in_user(self):
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token_user}')
        response = self.client.get(reverse('user-me'))
        serializer = UserSerializer(self.user_test)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, 200)
        
    # TEST CREATE ROUTE
    def test_create_user(self):
        response = self.client.post(self.url_register_user, self.data_user)
        self.assertTrue(User.objects.filter(email=self.data_user['email']))
        self.assertEqual(response.status_code, 201)
        
    def test_if_you_are_automatically_creating_the_customer_with_the_user(self):
        response = self.client.post(self.url_register_user, self.data_user)
        self.assertTrue(User.objects.filter(email=self.data_user['email']))
        self.assertTrue(Customer.objects.filter(email=self.data_user['email']))
        self.assertEqual(response.status_code, 201)
    
    # TEST EMAIL FIELD
    def test_if_an_error_appears_when_trying_to_create_the_user_without_the_email(self):
        del self.data_user['email']
        response = self.client.post(self.url_register_user, self.data_user)
        self.assertEqual(response.status_code, 400)
        
    def test_if_any_error_appears_when_trying_to_create_the_user_with_an_invalid_email(self):
        self.data_user['email'] = 'InvalidEmail@.com'
        response = self.client.post(self.url_register_user, self.data_user)
        self.assertEqual(response.status_code, 400)
    
    # TEST FIRST NAME FIELD   
    def test_if_an_error_appears_when_trying_to_create_the_user_without_the_first_name(self):
        del self.data_user['first_name']
        response = self.client.post(self.url_register_user, self.data_user)
        self.assertEqual(response.status_code, 400)
        
    def test_raises_an_error_when_trying_to_create_a_user_with_a_first_name_of_less_than_2_characters(self):
        self.data_user['first_name'] = 'a'
        response = self.client.post(self.url_register_user, self.data_user)
        self.assertEqual(response.status_code, 400)
        
    def test_raises_an_error_when_trying_to_create_a_user_with_a_first_name_of_more_than_100_characters(self):
        self.data_user['first_name'] = 'a' * 101
        response = self.client.post(self.url_register_user, self.data_user)
        self.assertEqual(response.status_code, 400)
    
    # TEST LAST NAME FIELD 
    def test_if_an_error_appears_when_trying_to_create_the_user_without_the_last_name(self):
        del self.data_user['last_name']
        response = self.client.post(self.url_register_user, self.data_user)
        self.assertEqual(response.status_code, 400)
        
    def test_raises_an_error_when_trying_to_create_a_user_with_a_last_name_of_less_than_3_characters(self):
        self.data_user['last_name'] = 'aa'
        response = self.client.post(self.url_register_user, self.data_user)
        self.assertEqual(response.status_code, 400)
        
    def test_raises_an_error_when_trying_to_create_a_user_with_a_last_name_of_more_than_100_characters(self):
        self.data_user['last_name'] = 'a' * 101
        response = self.client.post(self.url_register_user, self.data_user)
        self.assertEqual(response.status_code, 400)
    
    # TEST PASSWORD AND PASSWORD_CONFIRMATION FIELDS
    def test_if_an_error_appears_when_trying_to_create_the_user_without_the_password(self):
        del self.data_user['password']
        response = self.client.post(self.url_register_user, self.data_user)
        self.assertEqual(response.status_code, 400)
        
    def test_if_an_error_arises_when_trying_to_create_a_user_with_a_password_of_less_than_6_characters(self):
        self.data_user['password'] = '#Pas1'
        response = self.client.post(self.url_register_user, self.data_user)
        self.assertEqual(response.status_code, 400)
        
    def test_if_an_error_appears_when_trying_to_create_a_user_with_a_password_without_at_least_1_number(self):
        self.data_user['password'] = '#Password'
        response = self.client.post(self.url_register_user, self.data_user)
        self.assertEqual(response.status_code, 400)
        
    def test_if_an_error_appears_when_trying_to_create_a_user_with_a_password_without_at_least_1_special_character(self):
        self.data_user['password'] = 'Password123'
        response = self.client.post(self.url_register_user, self.data_user)
        self.assertEqual(response.status_code, 400)
               
    def test_if_an_error_appears_when_trying_to_create_the_user_without_the_password_confirmation(self):
        del self.data_user['password_confirmation']
        response = self.client.post(self.url_register_user, self.data_user)
        self.assertEqual(response.status_code, 400)
    
    def test_if_an_error_appears_when_trying_to_create_a_user_with_a_password_other_than_password_confirmation(self):
        self.data_user['password'] = '#Password123'
        self.data_user['password_confirmation'] = '@Password123'
        response = self.client.post(self.url_register_user, self.data_user)
        self.assertEqual(response.status_code, 400)
        
    # TEST UPDATE ROUTE
    def test_logged_in_user_update(self):
        self.data_user['current_password'] = '#Test11'
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token_user}')
        response = self.client.patch(reverse('user-me'), self.data_user)
        user = User.objects.get(id=self.user_test.id)
        self.assertEqual(user.email, self.data_user['email'])
        self.assertEqual(user.first_name, self.data_user['first_name'])
        self.assertEqual(user.last_name, self.data_user['last_name'])
        self.assertTrue(user.check_password(self.data_user['password']))
        self.assertEqual(response.status_code, 200)
        
    def test_update_email(self):
        data = {'email': 'updatedemail@gmail.com', 'current_password': '#Test11'}
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token_user}')
        response = self.client.patch(reverse('user-me'), data)
        user = User.objects.get(id=self.user_test.id)
        
        self.assertEqual(user.email, data['email'])
        self.assertEqual(response.status_code, 200)
        
    def test_update_first_name(self):
        data = {'first_name': 'UpdatedFirstName', 'current_password': '#Test11'}
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token_user}')
        response = self.client.patch(reverse('user-me'), data)
        user = User.objects.get(id=self.user_test.id)
        
        self.assertEqual(user.first_name, data['first_name'])
        self.assertEqual(response.status_code, 200)
        
    def test_update_last_name(self):
        data = {'last_name': 'UpdatedLastName', 'current_password': '#Test11'}
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token_user}')
        response = self.client.patch(reverse('user-me'), data)
        user = User.objects.get(id=self.user_test.id)
        
        self.assertEqual(user.last_name, data['last_name'])
        self.assertEqual(response.status_code, 200)

    def test_update_password(self):
        data = {
            'password': 'NewPassword#11',
            'password_confirmation': 'NewPassword#11',
            'current_password': '#Test11'
        }
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token_user}')
        response = self.client.patch(reverse('user-me'), data)
        user = User.objects.get(id=self.user_test.id)
        
        self.assertTrue(user.check_password(data['password']))
        self.assertEqual(response.status_code, 200)

    # TEST DELETE ROUTE
    def test_delete_logged_in_user(self):
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token_user}')
        response = self.client.delete(reverse('user-me'))
        self.assertFalse(User.objects.filter(email='TestUser@gmail.com', first_name='Robert', last_name='Garcia').exists())
        self.assertEqual(response.status_code, 204)