from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet
from product.models import Product,Category
from .serializers import CategorySerializer, ProductSerializer
from rest_framework.decorators import action
from review.serializers import LikeSerializer
from review.models import Like
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from rest_framework.permissions import IsAdminUser, AllowAny

class PermissionMixin():

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            permissions = [IsAdminUser, ]
        else:
            permissions = [AllowAny]
        return [permission() for permission in permissions]


class CategoryViewSet(PermissionMixin, ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class ProductViewSet(PermissionMixin, ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    search_fields = ['price']

    @action(methods=['POST'], detail=True)
    def like(self, request, pk=None):
        product = self.get_object()
        user = request.user
        serializer = LikeSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            try:
                like = Like.objects.get(product=product, author = user)
                like.delete()
                # like.is_liked = not like.is_liked
                # like.save()
                message = 'disliked'
            except Like.DoesNotExist:
                Like.objects.create(product=product, is_liked=True, author=user)
                message = 'liked'
            return Response(message, status=200)

