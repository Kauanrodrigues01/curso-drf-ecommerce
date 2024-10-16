from django.shortcuts import render
from rest_framework.decorators import api_view
from django.shortcuts import get_object_or_404
from .serializers import ProductSerializer
from storeapp.models import Product
from rest_framework.response import Response
from rest_framework import status
from rest_framework.exceptions import NotFound

@api_view()
def api_products(request):
    products = Product.objects.all()
    serializer = ProductSerializer(products, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view()
def api_product_detail(request, pk):
    try:
        product = Product.objects.get(id=pk)
    except Product.DoesNotExist:
        raise NotFound({'detail': 'product not found'})
    serializer = ProductSerializer(product)
    return Response(serializer.data)