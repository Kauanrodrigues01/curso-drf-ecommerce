from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet
from rest_framework.views import APIView
from storeapp.models import Product, Category
from .serializers import ProductSerializer, CategorySerializer
from rest_framework.exceptions import NotFound
from rest_framework.response import Response
from rest_framework import status
from .permissions import CategoriesPermissionsViews, ProductsPermissionsViews
from django.utils.crypto import get_random_string
from storeapp.models import Cart
from .serializers import CartSerializer

class ProductViewSet(ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [ProductsPermissionsViews,]
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
        
        # Adiciona o session_id aos dados que serão passados para o serializer
        data = {
            'session_id': session_id,
            'completed': False
        }

        # Cria um novo carrinho usando os dados fornecidos
        serializer = CartSerializer(data=data, context={'user': request.user})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)