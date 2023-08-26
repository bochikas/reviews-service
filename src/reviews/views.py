from django.contrib.auth import get_user_model
from drf_spectacular.utils import extend_schema, OpenApiResponse
from rest_framework import mixins, permissions, response, status, views, viewsets
from rest_framework.decorators import action

from reviews import serializers as api_serializers
from reviews import models as api_models
from reviews.permissions import IsAuthorOrReadOnlyPermission


User = get_user_model()


class SoftDeleteDestroyModelMixin(mixins.DestroyModelMixin):
    """Миксин с 'мягким' удалением."""

    def perform_destroy(self, instance):
        instance.deleted = True
        instance.save()


class CreateUserView(views.APIView):
    """Регистрация пользователей."""

    serializer = api_serializers.CreateUserSerializer

    @extend_schema(request=api_serializers.CreateUserSerializer,
                   responses={201: OpenApiResponse(response=api_serializers.IdResponseSerializer,
                                                   description='Created. Id in response'),
                              400: OpenApiResponse(description='Bad request')})
    def post(self, request):
        serializer = self.serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return response.Response({'id': serializer.instance.id}, status=status.HTTP_201_CREATED)


class UserViewSet(mixins.RetrieveModelMixin, mixins.ListModelMixin, viewsets.GenericViewSet):
    """Вьюсет пользователей."""

    queryset = User.objects.all()
    permission_classes = [permissions.IsAuthenticated]

    def get_serializer_class(self):
        if self.action in ('me', 'patch_me'):
            return api_serializers.UserEditSerializer
        return api_serializers.UserSerializer

    @action(detail=False, methods=['get'], permission_classes=[permissions.IsAuthenticated])
    def me(self, request, *args, **kwargs):
        """Информация о себе."""

        instance = self.request.user
        serializer = self.get_serializer(instance)
        return response.Response(serializer.data)

    @me.mapping.patch
    def patch_me(self, request, ser):
        """Редактирование своих данных."""

        instance = self.request.user
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return response.Response(serializer.data)


class ReviewViewSet(SoftDeleteDestroyModelMixin, viewsets.ModelViewSet):
    """Вьюсет обзоров."""

    permission_classes = [permissions.IsAuthenticated & (IsAuthorOrReadOnlyPermission | permissions.IsAdminUser)]

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
