from rest_framework import serializers
from storeapp.models import Category, Product
from utils import validate_string_field

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'name', 'description', 'category', 'slug', 'inventory', 'old_price', 'price', 'image', 'discount', 'top_deal', 'flash_sales']

    def validate(self, attrs):
        required_fields = ['name', 'slug', 'inventory', 'old_price']
        request = self.context.get('request')
        
        for field in required_fields:
            if request.method == 'PATCH':
                if attrs.get(field) is None and hasattr(self.instance, field):
                    attrs[field] = getattr(self.instance, field)
            else:
                if attrs.get(field) is None:
                    raise serializers.ValidationError({field: f'The {field} field cannot be null'})


        validate_string_field('name', attrs.get('name'), min_length=3, max_length=200)

        description = attrs.get('description', None)
        if description is not None:
            validate_string_field('description', description, min_length=10, max_length=800)

        validate_string_field('slug', attrs.get('slug'), min_length=3, max_length=100)

        return attrs

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['category_id', 'title', 'slug', 'featured_product', 'icon']

    def validate(self, attrs):
        required_fields = ['title', 'slug']
        request = self.context.get('request')
        
        for field in required_fields:
            if request.method == 'PATCH':
                if attrs.get(field) is None and hasattr(self.instance, field):
                    attrs[field] = getattr(self.instance, field)
            if attrs.get(field) is None:
                raise serializers.ValidationError({field: f'The {field} field cannot be null'})

        validate_string_field('title', attrs.get('title'), min_length=3, max_length=200)

        validate_string_field('slug', attrs.get('slug'), min_length=3, max_length=100)

        icon = attrs.get('icon')
        if icon is not None and len(icon) > 100:
            raise serializers.ValidationError({'icon': 'Must have a maximum of 100 characters'})

        return attrs
