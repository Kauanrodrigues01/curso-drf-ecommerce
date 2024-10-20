from rest_framework.viewsets import ModelViewSet
from storeapp.models import Product, Category
from .serializers import ProductSerializer, CategorySerializer
from rest_framework.exceptions import NotFound
from rest_framework.response import Response
from .permissions import CategoriesPermissionsViews, ProductsPermissionsViews

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