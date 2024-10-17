from django.urls import path
from .views import ProductListView, ProductDetailView, CategoryListView, CategoryDetailView

urlpatterns = [
    # Rotas para produtos
    path('products', ProductListView.as_view(), name='product-list'),
    path('products/<uuid:id>', ProductDetailView.as_view(), name='product-detail'),

    # Rotas para categorias
    path('categories', CategoryListView.as_view(), name='category-list'),
    path('categories/<uuid:category_id>', CategoryDetailView.as_view(), name='category-detail'),
]
