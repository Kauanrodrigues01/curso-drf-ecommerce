from rest_framework.routers import DefaultRouter
from django.urls import path, include
from .views import ProductViewSet, CategoryViewSet
from .views_users import UserCreateView, UserDetailMeView, UserViewAdmin

router = DefaultRouter()
router.register(r'products', ProductViewSet, basename='product')
router.register(r'categories', CategoryViewSet, basename='category')

urlpatterns = [
    path('', include(router.urls)),
    path('user/register/', UserCreateView.as_view(), name='user-register'),
    path('user/me/', UserDetailMeView.as_view(), name='user-me'),
    path('user/', UserViewAdmin.as_view({'get': 'list'}), name='user-list'),
    path('user/<int:id>/', UserViewAdmin.as_view({'get': 'retrieve'}), name='user-detail')
]
