import email
from rest_framework import serializers
from storeapp.models import Category, Product
from utils import validate_string_field, validate_password_strength
from core.models import User
from UserProfile.models import Customer
from collections import defaultdict

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'name', 'description', 'category', 'slug', 'inventory', 'old_price', 'price', 'image', 'discount', 'top_deal', 'flash_sales']

    def validate(self, attrs):
        required_fields = ['name', 'slug', 'inventory', 'old_price']
        request = self.context.get('request')
        errors = defaultdict(list)
        
        for field in required_fields:
            if request.method == 'PATCH':
                if attrs.get(field) is None and hasattr(self.instance, field):
                    attrs[field] = getattr(self.instance, field)
            else:
                if attrs.get(field) is None:
                    errors[field].append(f'The {field} field cannot be null')

        errors = validate_string_field('name', attrs.get('name'), min_length=3, max_length=200, list_of_errors=errors)

        description = attrs.get('description', None)
        if description is not None:
            errors = validate_string_field('description', description, min_length=10, max_length=800, list_of_errors=errors)

        if not attrs.get('slug') is None:
            errors = validate_string_field('slug', attrs.get('slug'), min_length=3, max_length=100, list_of_errors=errors)

        if errors:
            raise serializers.ValidationError(errors)

        return attrs


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['category_id', 'title', 'slug', 'featured_product', 'icon']

    def validate(self, attrs):
        required_fields = ['title', 'slug']
        request = self.context.get('request')
        errors = defaultdict(list)
        
        for field in required_fields:
            if request.method == 'PATCH':
                if attrs.get(field) is None and hasattr(self.instance, field):
                    attrs[field] = getattr(self.instance, field)
            if attrs.get(field) is None:
                errors[field].append(f'The {field} field cannot be null')

        errors = validate_string_field('title', attrs.get('title'), min_length=3, max_length=200, list_of_errors=errors)
        
        if not attrs.get('slug') is None:
            errors = validate_string_field('slug', attrs.get('slug'), min_length=3, max_length=100, list_of_errors=errors)

        icon = attrs.get('icon')
        if icon is not None and len(icon) > 100:
            errors['icon'].append('Must have a maximum of 100 characters')

        if errors:
            raise serializers.ValidationError(errors)

        return attrs


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    password_confirmation = serializers.CharField(write_only=True)
    
    class Meta:
        model = User
        fields = ['id', 'email', 'first_name', 'last_name', 'password', 'password_confirmation']
        
    def validate(self, attrs):
        required_fields = ['email', 'first_name', 'last_name', 'password', 'password_confirmation']
        request = self.context.get('request')
        errors = defaultdict(list)
        
        for field in required_fields:
            if request.method == 'PATCH':
                if attrs.get(field) is None and hasattr(self.instance, field):
                    attrs[field] = getattr(self.instance, field)
            if attrs.get(field) is None:
                errors[field].append(f'The {field} field cannot be null')
        
        first_name = attrs.get('first_name')
        last_name = attrs.get('last_name')
        password = attrs.get('password').strip()
        password_confirmation = attrs.get('password_confirmation').strip()
        
        errors = validate_string_field('first_name', first_name, min_length=1, max_length=100, list_of_errors=errors)
        errors = validate_string_field('last_name', last_name, min_length=1, max_length=100, list_of_errors=errors)
        errors = validate_password_strength(password, list_of_errors=errors)
        
        if password != password_confirmation:
            errors['password_confirmation'].append("The two password fields didn’t match.")
        
        if errors:
            raise serializers.ValidationError(errors)
        
        return attrs
    
    def create(self, validated_data):
        password = validated_data.pop('password')
        validated_data.pop('password_confirmation')
        
        user = User.objects.create_user(**validated_data)
        user.set_password(password)
        user.save()
        
        return user