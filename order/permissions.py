from rest_framework.permissions import BasePermission, AllowAny


class IsAuthorOrReadOnly(BasePermission):
    def has_object_permission(self, request, view, obj):
        return request.user.is_authenticated and request.user == obj.author


class PermissionMixin():

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            permissions = [IsAuthorOrReadOnly, ]
        else:
            permissions = [AllowAny, ]
        return [permission() for permission in permissions]