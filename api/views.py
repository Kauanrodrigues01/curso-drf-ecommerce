from rest_framework.viewsets import ModelViewSet
from rest_framework.generics import ListAPIView, CreateAPIView
from storeapp.models import Product, Category
from .serializers import ProductSerializer, CategorySerializer, UserSerializer
from rest_framework.exceptions import NotFound
from rest_framework.response import Response
from core.models import User

class ProductViewSet(ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    lookup_field = 'id'  # Mantemos o campo de busca como 'id'

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
    lookup_field = 'category_id'  # Mantemos o campo de busca como 'category_id'

    def retrieve(self, request, *args, **kwargs):
        try:
            instance = self.get_queryset().get(category_id=kwargs['category_id'])
        except Category.DoesNotExist:
            raise NotFound({'detail': 'Category Not Found'})
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

class UserCreateView(CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    http_method_names = ['post']