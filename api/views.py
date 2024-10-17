from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from storeapp.models import Product
from .serializers import ProductSerializer
from storeapp.models import Category
from .serializers import CategorySerializer
from rest_framework.exceptions import NotFound
from rest_framework.response import Response

class ProductListView(ListCreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

class ProductDetailView(RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    lookup_field = 'id'
    
    def retrieve(self, request, *args, **kwargs):
        try:
            instance = self.get_queryset().get(id=kwargs['id'])
        except Product.DoesNotExist:
            raise NotFound({'detail': 'Product Not Found'})
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

class CategoryListView(ListCreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

class CategoryDetailView(RetrieveUpdateDestroyAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    lookup_field = 'category_id'
    
    def retrieve(self, request, *args, **kwargs):
        try:
            instance = self.get_queryset().get(category_id=kwargs['category_id'])
        except Category.DoesNotExist:
            raise NotFound({'detail': 'Category Not Found'})
        serializer = self.get_serializer(instance)
        return Response(serializer.data)
