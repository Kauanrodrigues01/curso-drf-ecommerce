from rest_framework.routers import DefaultRouter
from django.urls import path, include
from .views import ProductViewSet, CategoryViewSet, UserCreateView, UserDetailView

router = DefaultRouter()
router.register(r'products', ProductViewSet, basename='product')
router.register(r'categories', CategoryViewSet, basename='category')

urlpatterns = [
    path('', include(router.urls)),
    path('user/register/', UserCreateView.as_view(), name='user-register'),
    path('user/me/', UserDetailView.as_view(), name='user-me')
]
