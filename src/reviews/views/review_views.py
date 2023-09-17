from rest_framework import permissions, response, status, viewsets

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
        return api_models.Review.objects.active()

    def get_serializer_class(self):
        if self.action in ('create', 'update', 'partial_update'):
            return api_serializers.ReviewWriteSerializer
        return api_serializers.ReviewReadSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        instance = services.create_update_review(serializer.validated_data, author=request.user)
        return response.Response(self.get_serializer_class()(instance).data, status=status.HTTP_201_CREATED)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        services.create_update_review(serializer.validated_data, author=request.user, instance=instance)

        if getattr(instance, '_prefetched_objects_cache', None):
            # If 'prefetch_related' has been applied to a queryset, we need to
            # forcibly invalidate the prefetch cache on the instance.
            instance._prefetched_objects_cache = {}

        instance.refresh_from_db()
        return response.Response(self.get_serializer_class()(instance).data)


class CategoryViewSet(SoftDeleteDestroyModelMixin, viewsets.ModelViewSet):
    """Вьюсет категорий."""

    queryset = api_models.Category.objects.all()
    serializer_class = api_serializers.CategorySerializer
