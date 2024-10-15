import django.db.models.signals
from django.shortcuts import render
import rest_framework
from rest_framework.decorators import api_view
from django.shortcuts import get_object_or_404
from .serializers import ProductSerializer
from storeapp.models import Product
from rest_framework.response import Response
from rest_framework import status

@api_view()
def api_products(request):
    products = Product.objects.all()
    serializer = ProductSerializer(products, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)