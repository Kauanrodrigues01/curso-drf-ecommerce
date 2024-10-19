from rest_framework.permissions import BasePermission, SAFE_METHODS

class ProductsPermissionsViews(BasePermission):
    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True
        if request.method in ('PATCH', 'DELETE', 'POST'):
            return request.user.is_authenticated and request.user.is_staff
        return super().has_permission(request, view)
    
class CategoriesPermissionsViews(BasePermission):
    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True
        if request.method in ('PATCH', 'DELETE', 'POST'):
            return request.user.is_authenticated and request.user.is_staff
        return super().has_permission(request, view)
    
class UserCreatePermissionView(BasePermission):
    def has_permission(self, request, view):
        return not request.user.is_authenticated
