from rest_framework import permissions, viewsets

from reviews import models as api_models, serializers as api_serializers, services
from reviews.filters import ReviewFilter
from reviews.permissions import IsAuthorOrReadOnlyPermission
from .mixins import SoftDeleteDestroyModelMixin


class ReviewViewSet(SoftDeleteDestroyModelMixin, viewsets.ModelViewSet):
    """Вьюсет обзоров."""

    permission_classes = [permissions.IsAuthenticated & (IsAuthorOrReadOnlyPermission | permissions.IsAdminUser)]
    filterset_class = ReviewFilter

    def get_queryset(self):
        if getattr(self, 'swagger_fake_view', False):  # для правильной работы drf-spectacular
            return api_models.Review.objects.none()
        return api_models.Review.objects.active_select_prefetch()

    def get_serializer_class(self):
        if self.action in ('create', 'update', 'partial_update'):
            return api_serializers.ReviewWriteSerializer
        return api_serializers.ReviewReadSerializer

    def perform_create(self, serializer):
        instance = services.create_update_review(serializer.validated_data)
        serializer.instance = instance

    def perform_update(self, serializer):
        services.create_update_review(serializer.validated_data, instance=serializer.instance)


class CategoryViewSet(SoftDeleteDestroyModelMixin, viewsets.ModelViewSet):
    """Вьюсет категорий."""

    permission_classes = [permissions.IsAuthenticated & permissions.IsAdminUser]

    def get_queryset(self):
        if getattr(self, 'swagger_fake_view', False):  # для правильной работы drf-spectacular
            return api_models.Category.objects.none()
        return api_models.Category.objects.active()

    def get_serializer_class(self):
        if self.action in ('create', 'update', 'partial_update'):
            return api_serializers.CategoryWriteSerializer
        return api_serializers.CategoryReadSerializer
