from django.urls import path,include
from .views import RatingViewSet, CommentViewSet
from rest_framework.routers import DefaultRouter


router = DefaultRouter()
router.register('ratings', RatingViewSet)
router.register('comments', CommentViewSet)

urlpatterns = [
    path('',include(router.urls)),
]