import email
from rest_framework import serializers
from storeapp.models import Category, Product
from utils import validate_string_field, validate_password_strength
from core.models import User
from UserProfile.models import Customer
from collections import defaultdict
from django.utils.translation import gettext_lazy as _
from storeapp.models import Cart, Cartitems, SavedItem

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'name', 'description', 'category', 'slug', 'inventory', 'old_price', 'price', 'image', 'discount', 'top_deal', 'flash_sales']
        read_only_fields = ['price']

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
            if attrs.get(field) is None:
                errors[field].append(f'The {field} field cannot be null')
        
        first_name = attrs.get('first_name')
        last_name = attrs.get('last_name')
        password = attrs.get('password').strip() if attrs.get('password') is not None else None
        password_confirmation = attrs.get('password_confirmation').strip() if attrs.get('password_confirmation') is not None else None
        
        errors = validate_string_field('first_name', first_name, min_length=2, max_length=100, list_of_errors=errors)
        errors = validate_string_field('last_name', last_name, min_length=3, max_length=100, list_of_errors=errors)
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
    
    def update(self, instance, validated_data):
        instance.email = validated_data.get('email', instance.email)
        instance.first_name = validated_data.get('first_name', instance.first_name)
        instance.last_name = validated_data.get('last_name', instance.last_name)
        
        password = validated_data.get('password', None)
        if password:
            instance.set_password(password)
        
        instance.save()

        return instance

class UserUpdateSerializer(serializers.ModelSerializer):
    current_password = serializers.CharField(write_only=True, required=False)
    password = serializers.CharField(write_only=True, required=False)
    password_confirmation = serializers.CharField(write_only=True, required=False)

    class Meta:
        model = User
        fields = ['email', 'first_name', 'last_name', 'current_password', 'password', 'password_confirmation']
    
    def validate(self, attrs):
        user = self.context.get('user')
        current_password = attrs.get('current_password')
        password = attrs.get('password')
        password_confirmation = attrs.get('password_confirmation')
        errors = defaultdict(list)

        if 'email' in attrs or 'first_name' in attrs or 'last_name' in attrs:
            if not current_password:
                errors['current_password'].append(_("You must provide the current password to update your profile information."))
            elif not user.check_password(current_password):
                errors['current_password'].append(_("The current password is incorrect."))

        # Verifica a atualização da senha
        if password or password_confirmation:
            if not password:
                errors['password'].append(_("Password is required."))
            elif password != password_confirmation:
                errors['password_confirmation'].append(_("The two password fields didn't match."))
            if password:
                errors = validate_password_strength(password, list_of_errors=errors)
            

        # Se houver erros, levanta uma exceção de validação com todos eles
        if errors:
            raise serializers.ValidationError(errors)

        return attrs

    def update(self, instance, validated_data):
        instance.email = validated_data.get('email', instance.email)
        instance.first_name = validated_data.get('first_name', instance.first_name)
        instance.last_name = validated_data.get('last_name', instance.last_name)

        password = validated_data.get('password')
        if password:
            instance.set_password(password)

        instance.save()
        return instance
    
    
class CartSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cart
        fields = ['cart_id', 'owner', 'created', 'completed', 'session_id', 'num_of_items', 'cart_total']
        read_only_fields = ['cart_id', 'created', 'num_of_items', 'cart_total', 'owner']

    def validate(self, attrs):
        errors = defaultdict(list)
        user = self.context.get('user')
        customer = Customer.objects.get(user=user)
        
        if Cart.objects.filter(owner=customer).exists():
            raise serializers.ValidationError({'error': 'There is already a cart with this customer'})
        
        # Validação do campo 'completed'
        completed = attrs.get('completed')
        if completed not in [True, False]:
            errors['completed'].append('The completed field must be True or False.')
        
        # Verificação de session_id
        if attrs.get('session_id') is None:
            errors['session_id'].append('Session ID cannot be null.')
            
        attrs['owner'] = customer

        # Caso haja algum erro, ele será levantado
        if errors:
            raise serializers.ValidationError(errors)

        return attrs


class CartitemsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cartitems
        fields = ['id', 'cart', 'product', 'quantity', 'subTotal']
        read_only_fields = ['subTotal']

    def validate(self, attrs):
        errors = defaultdict(list)
        product = attrs.get('product')
        quantity = attrs.get('quantity')
        
        if quantity is not None and quantity <= 0:
            errors['quantity'].append('Quantity must be greater than zero.')

        if not product and not self.instance:
            errors['product'].append('Product cannot be null.')
            
        if product is not None and quantity is not None:
            if quantity > product.inventory:
                errors['quantity'].append('Desired quantity exceeds available inventory.')
                
        if errors:
            raise serializers.ValidationError(errors)

        return attrs

    def create(self, validated_data):
        cart = validated_data.get('cart')
        product = validated_data.get('product')
        quantity = validated_data.get('quantity', 1)

        # Tenta buscar o item no carrinho, se já existir, atualiza a quantidade
        cart_item, created = Cartitems.objects.get_or_create(
            cart=cart,
            product=product,
            defaults={'quantity': quantity}
        )
        

        # Se o item já existe no carrinho, atualiza a quantidade
        if not created:
            if (quantity + cart_item.quantity) > product.inventory:
                raise serializers.ValidationError({
                    'quantity': 'Desired quantity exceeds available inventory.'
                })
            cart_item.quantity += quantity
            cart_item.save()

        return cart_item

    def update(self, instance, validated_data):
        quantity = validated_data.get('quantity', instance.quantity)
        instance.quantity = quantity
        instance.save()
        return instance
    
    
class SavedItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = SavedItem
        fields = ['id', 'owner', 'product', 'added']
    
    def validate(self, attrs):
        errors = defaultdict(list)
        
        # Verificação se o campo 'product' está vazio
        if attrs.get('product') is None:
            errors['product'].append('Product cannot be null.')
        
        # Verificação para 'added'
        added = attrs.get('added')
        if added is not None and added < 0:
            errors['added'].append('Added value must be greater or equal to zero.')

        # Caso haja algum erro, ele será levantado
        if errors:
            raise serializers.ValidationError(errors)
        
        return attrs

    def update(self, instance, validated_data):
        # Atualização parcial
        for field, value in validated_data.items():
            setattr(instance, field, value)
        instance.save()
        return instance