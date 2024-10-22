import django_filters as filters
from storeapp.models import Category, Product

class CategoryFilter(filters.FilterSet):
    title = filters.CharFilter(field_name='title', lookup_expr='icontains')
    slug = filters.CharFilter(field_name='slug', lookup_expr='icontains')

    class Meta:
        model = Category
        fields = ['title', 'slug', 'featured_product']


class ProductFilter(filters.FilterSet):
    name = filters.CharFilter(field_name='name', lookup_expr='icontains')
    category = filters.CharFilter(field_name='category__title', lookup_expr='icontains')
    discount = filters.BooleanFilter(field_name='discount')
    top_deal = filters.BooleanFilter(field_name='top_deal')
    
    class Meta:
        model = Product
        fields = ['name', 'category', 'discount', 'top_deal']
