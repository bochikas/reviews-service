from rest_framework import permissions, viewsets

from reviews import models as api_models
from reviews import serializers as api_serializers
from reviews.filters import ReviewFilter
from reviews.permissions import IsAuthorOrReadOnlyPermission
from .mixins import SoftDeleteDestroyModelMixin


class ReviewViewSet(SoftDeleteDestroyModelMixin, viewsets.ModelViewSet):
    """Вьюсет обзоров."""

    permission_classes = [permissions.IsAuthenticated & (IsAuthorOrReadOnlyPermission | permissions.IsAdminUser)]
    filterset_class = ReviewFilter

    def get_queryset(self):
        if getattr(self, 'swagger_fake_view', False):
            return api_models.Review.objects.none()
        return api_models.Review.objects.select_related('author', 'product')

    def get_serializer_class(self):
        if self.action in ('create', 'update', 'partial_update'):
            return api_serializers.ReviewWriteSerializer
        return api_serializers.ReviewReadSerializer


class CategoryViewSet(SoftDeleteDestroyModelMixin, viewsets.ModelViewSet):
    """Вьюсет категорий."""

    queryset = api_models.Category.objects.all()
    serializer_class = api_serializers.CategorySerializer
