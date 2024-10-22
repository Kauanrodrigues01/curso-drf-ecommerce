from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet
from rest_framework.views import APIView
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from storeapp.models import Product, Category, Cart, Cartitems, SavedItem
from .serializers import ProductSerializer, CategorySerializer, CartSerializer, CartitemsSerializer, SavedItemSerializer
from rest_framework.exceptions import NotFound
from rest_framework.response import Response
from rest_framework import status
from .permissions import CategoriesPermissionsViews, ProductsPermissionsViews
from django.utils.crypto import get_random_string
from UserProfile.models import Customer
from django_filters.rest_framework import DjangoFilterBackend
from .filters import ProductFilter, CategoryFilter

class ProductViewSet(ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [ProductsPermissionsViews,]
    filter_backends = [DjangoFilterBackend]
    filterset_class = ProductFilter
    lookup_field = 'id' 

    def retrieve(self, request, *args, **kwargs):
        try:
            instance = self.get_queryset().get(id=kwargs['id'])
        except Product.DoesNotExist:
            raise NotFound({'detail': 'Product Not Found'})
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

class CategoryViewSet(ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [CategoriesPermissionsViews,]
    filter_backends = [DjangoFilterBackend]
    filterset_class = CategoryFilter
    lookup_field = 'category_id'

    def retrieve(self, request, *args, **kwargs):
        try:
            instance = self.get_queryset().get(category_id=kwargs['category_id'])
        except Category.DoesNotExist:
            raise NotFound({'detail': 'Category Not Found'})
        serializer = self.get_serializer(instance)
        return Response(serializer.data)


class CartView(APIView):
    permission_classes = [IsAuthenticated]
    
    def post(self, request, *args, **kwargs):
        # Verifica se já existe uma session_key, se não, gera uma
        if not request.session.session_key:
            request.session.create()

        # Obtém o session_id da sessão atual ou gera uma nova chave
        session_id = request.session.session_key or get_random_string(32)
        
        data = {
            'session_id': session_id,
            'completed': False
        }

        serializer = CartSerializer(data=data, context={'user': request.user})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def get(self, request):
        user = request.user
        customer = Customer.objects.get(user=user)
        
        try:
            cart = Cart.objects.get(owner=customer)
            serializer = CartSerializer(cart)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Cart.DoesNotExist:
            return Response(
                {"detail": "Carrinho não encontrado."},
                status=status.HTTP_404_NOT_FOUND
            )
            
class CartitemsView(ListCreateAPIView):
    serializer_class = CartitemsSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        customer = Customer.objects.get(user=user)
        cart = Cart.objects.filter(owner=customer).first()
        if not cart:
            raise NotFound(detail="Cart not found.")
        return Cartitems.objects.filter(cart=cart)

    def create(self, request, *args, **kwargs):
        user = request.user
        customer = Customer.objects.get(user=user)
        
        # Busca ou cria o carrinho do cliente
        cart = Cart.objects.filter(owner=customer).first()
        if not cart:
            return Response({"detail": "Cart not found."}, status=status.HTTP_404_NOT_FOUND)

        # Adiciona o ID do carrinho nos dados que serão enviados ao serializer
        data = request.data.copy()
        data['cart'] = cart.cart_id

        # Cria ou atualiza o CartItem via serializer
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
class CartitemsDetailView(RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated]
    http_method_names = ['patch', 'delete']
    serializer_class = CartitemsSerializer
    lookup_field = 'id'
    
    def patch(self, request, id):
        quantity = request.data.get('quantity')
        data = {
            'quantity': quantity
        }
        
        try:
            cart_items = Cartitems.objects.get(id=id)
        except Cartitems.DoesNotExist:
            return Response({"detail": "Cartitem not found."}, status=status.HTTP_404_NOT_FOUND)

        serializer = self.get_serializer(cart_items, data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, id):
        try:
            cart_items = Cartitems.objects.get(id=id)
        except Cartitems.DoesNotExist:
            return Response({"detail": "Cartitem not found."}, status=status.HTTP_404_NOT_FOUND)

        cart_items.delete()
        return Response([], status=status.HTTP_204_NO_CONTENT)


class SavedItemViewSet(ModelViewSet):
    queryset = SavedItem.objects.all()
    serializer_class = SavedItemSerializer
    permission_classes = [IsAuthenticated]
    http_method_names = ['get', 'post', 'delete']

    def get_queryset(self):
        customer = Customer.objects.get(user=self.request.user)
        return SavedItem.objects.filter(owner=customer)

    def perform_create(self, serializer):
        customer = Customer.objects.get(user=self.request.user)
        serializer.save(owner=customer)