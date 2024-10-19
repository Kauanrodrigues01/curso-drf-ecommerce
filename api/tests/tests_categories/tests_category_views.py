from api.tests.tests_categories.base.test_base_category_views import TestBaseCategoryViews
from storeapp.models import Category
from django.urls import reverse
from api.serializers import CategorySerializer

class TestCategoryViews(TestBaseCategoryViews):
    def test_list_categories(self):
        response = self.client.get(reverse('category-list'))
        serializer_category1 = CategorySerializer(Category.objects.get(category_id=self.category1.category_id))
        self.assertIn(serializer_category1.data, response.data)
        self.assertEqual(response.status_code, 200)
        
    def test_detail_category(self):
        response = self.client.get(reverse('category-detail', kwargs={'category_id': self.category1.category_id}))
        serializer_category1 = CategorySerializer(Category.objects.get(category_id=self.category1.category_id))
        self.assertEqual(serializer_category1.data, response.data)
        self.assertEqual(response.status_code, 200)
        
    def test_create_category(self):
        response = self.client.post(reverse('category-list'), self.data)
        self.assertTrue(Category.objects.filter(title=self.data['title'], slug=self.data['slug']).exists())
        self.assertEqual(response.status_code, 201)
    
    # TEST TITLE FIELD 
    def test_if_an_error_appears_when_trying_to_create_a_category_without_the_title(self):
        del self.data['title']
        response = self.client.post(reverse('category-list'), self.data)
        self.assertEqual(response.status_code, 400)
        
    def test_if_an_error_appears_when_trying_to_create_a_category_with_title_with_less_than_3_characters(self):
        self.data['title'] = 'aa'
        response = self.client.post(reverse('category-list'), self.data)
        self.assertEqual(response.status_code, 400)
        
    def test_if_an_error_appears_when_trying_to_create_a_category_with_title_with_more_than_200_characters(self):
        self.data['title'] = 'a' * 201
        response = self.client.post(reverse('category-list'), self.data)
        self.assertEqual(response.status_code, 400)
        
    def test_if_an_error_appears_when_trying_to_create_a_category_with_title_with_just_numbers(self):
        self.data['title'] = '111111'
        response = self.client.post(reverse('category-list'), self.data)
        self.assertEqual(response.status_code, 400)
        
    def test_if_an_error_appears_when_trying_to_create_a_category_with_an_empty_title(self):
        self.data['title'] = ''
        response = self.client.post(reverse('category-list'), self.data)
        self.assertEqual(response.status_code, 400)
    
    # TEST SLUG FIELD
    def test_if_an_error_appears_when_trying_to_create_a_category_without_the_slug(self):
        del self.data['slug']
        response = self.client.post(reverse('category-list'), self.data)
        self.assertEqual(response.status_code, 400)
        
    def test_if_an_error_appears_when_trying_to_create_a_category_with_slug_with_less_than_3_characters(self):
        self.data['slug'] = 'aa'
        response = self.client.post(reverse('category-list'), self.data)
        self.assertEqual(response.status_code, 400)
        
    def test_if_an_error_appears_when_trying_to_create_a_category_with_slug_with_more_than_100_characters(self):
        self.data['slug'] = 'a' * 101
        response = self.client.post(reverse('category-list'), self.data)
        self.assertEqual(response.status_code, 400)
        
    def test_if_an_error_appears_when_trying_to_create_a_category_with_slug_with_just_numbers(self):
        self.data['slug'] = '111111'
        response = self.client.post(reverse('category-list'), self.data)
        self.assertEqual(response.status_code, 400)
        
    def test_if_an_error_appears_when_trying_to_create_a_category_with_an_empty_slug(self):
        self.data['slug'] = ''
        response = self.client.post(reverse('category-list'), self.data)
        self.assertEqual(response.status_code, 400)
      
    def test_category_update(self):
        response = self.client.patch(reverse('category-detail', kwargs={'category_id': self.category1.category_id}), self.data)
        serializer_category1 = CategorySerializer(Category.objects.get(category_id=self.category1.category_id))
        self.assertEqual(serializer_category1.data, response.data)
        self.assertEqual(response.status_code, 200)
        
    def test_category_title_update(self):
        self.data = {'title': self.data['title']}
        response = self.client.patch(reverse('category-detail', kwargs={'category_id': self.category1.category_id}), self.data)
        serializer_category1 = CategorySerializer(Category.objects.get(category_id=self.category1.category_id))
        self.assertEqual(serializer_category1.data, response.data)
        self.assertEqual(response.status_code, 200)
        
    def test_category_slug_update(self):
        self.data = {'slug': self.data['slug']}
        response = self.client.patch(reverse('category-detail', kwargs={'category_id': self.category1.category_id}), self.data)
        serializer_category1 = CategorySerializer(Category.objects.get(category_id=self.category1.category_id))
        self.assertEqual(serializer_category1.data, response.data)
        self.assertEqual(response.status_code, 200)
                
    def test_delete_category(self):
        response = self.client.delete(reverse('category-detail', kwargs={'category_id': self.category1.category_id}), self.data)
        self.assertFalse(Category.objects.filter(category_id=self.category1.category_id).exists())
        self.assertEqual(response.status_code, 204)