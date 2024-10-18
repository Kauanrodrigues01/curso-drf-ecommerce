from rest_framework.test import APIClient
from django.test import TestCase
from storeapp.models import Category

class TestBaseCategoryViews(TestCase):
    def setUp(self):
        self.client = APIClient()
        
        self.category1 = Category.objects.create(
            title='Category test 1',
            slug='category-test-1',
            icon='icon1.png'
        )

        self.category2 = Category.objects.create(
            title='Category test 2',
            slug='category-test-2',
            icon='icon2.png'
        )

        self.category3 = Category.objects.create(
            title='Category test 3',
            slug='category-test-3',
            icon='icon3.png'
        )
        
        self.data =  {
            'title': 'Category test',
            'slug': 'category-test',
            'icon': 'icon4.png'
        }
        
        return super().setUp()