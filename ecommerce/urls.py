from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenBlacklistView
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('storeapp.urls')),
    path('user/', include('UserProfile.urls')),
    path('api/', include('api.urls')),
    path('api/user/login/', TokenObtainPairView.as_view(), name='login'),
    path('api/user/refresh-token/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/user/logout/', TokenBlacklistView.as_view(), name='logout')
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
