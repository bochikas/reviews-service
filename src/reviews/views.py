from drf_spectacular.utils import extend_schema, OpenApiResponse
from rest_framework import permissions, response, status, views, viewsets

from reviews import serializers as api_serializers
from reviews import models as api_models
from reviews.permissions import IsAuthorOrReadOnlyPermission


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


class ReviewViewSet(viewsets.ModelViewSet):
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


class CategoryViewSet(viewsets.ModelViewSet):
    """Вьюсет категорий."""

    queryset = api_models.Category.objects.all()
    serializer_class = api_serializers.CategorySerializer
