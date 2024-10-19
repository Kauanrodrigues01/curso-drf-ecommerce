from UserProfile.models import Customer
from core.models import User
import email
from api.tests.tests_users.base.test_base_user_views import TestBaseUserViews
from django.urls import reverse

class TestUserViews(TestBaseUserViews):
    def test_create_user(self):
        response = self.client.post(self.url_register_user, self.data_user)
        self.assertTrue(User.objects.filter(email=self.data_user['email']))
        self.assertEqual(response.status_code, 201)
        
    def test_if_you_are_automatically_creating_the_customer_with_the_user(self):
        response = self.client.post(self.url_register_user, self.data_user)
        self.assertTrue(User.objects.filter(email=self.data_user['email']))
        self.assertTrue(Customer.objects.filter(email=self.data_user['email']))
        self.assertEqual(response.status_code, 201)
        
    def test_if_an_error_appears_when_trying_to_create_the_user_without_the_email(self):
        del self.data_user['email']
        response = self.client.post(self.url_register_user, self.data_user)
        self.assertEqual(response.status_code, 400)
        
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