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
from order.serializers import FavoriteSerializer
from order.models import Favorite

class PermissionMixin():

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            permissions = [IsAdminUser]
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


    @action(methods=['POST'], detail=True)
    def favorite(self, request, pk=None):
        product = self.get_object()
        author = request.user
        serializer = FavoriteSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            try:
                favorite = Favorite.objects.get(product=product, author=author)
                favorite.delete()
                message = 'deleted from favorites'
            except Favorite.DoesNotExist:
                Favorite.objects.create(product=product, author=author, is_favorite=True)
                message = 'added to favorites'
            return Response(message, status=200)
        
