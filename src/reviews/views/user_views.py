from django.contrib.auth import get_user_model
from drf_spectacular.utils import extend_schema, OpenApiResponse
from rest_framework import mixins, permissions, response, status, views, viewsets
from rest_framework.decorators import action

from reviews.serializers import IdResponseSerializer, UserSerializer, UserEditSerializer

User = get_user_model()


class CreateUserView(views.APIView):
    """Регистрация пользователей."""

    @extend_schema(request=UserSerializer,
                   responses={201: OpenApiResponse(response=IdResponseSerializer,
                                                   description='Created. Id in response'),
                              400: OpenApiResponse(description='Bad request')})
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = User.objects.create_new(serializer.validated_data)
        return response.Response({'id': user.id}, status=status.HTTP_201_CREATED)


class UserViewSet(mixins.RetrieveModelMixin, mixins.ListModelMixin, viewsets.GenericViewSet):
    """Вьюсет пользователей."""

    queryset = User.objects.active()
    permission_classes = [permissions.IsAuthenticated]

    def get_serializer_class(self):
        if self.action in ('me', 'patch_me'):
            return UserEditSerializer
        return UserSerializer

    @action(detail=False, methods=['get'], permission_classes=[permissions.IsAuthenticated])
    def me(self, request, *args, **kwargs):
        """Информация о себе."""

        instance = self.request.user
        serializer = self.get_serializer(instance)
        return response.Response(serializer.data)

    @me.mapping.patch
    def patch_me(self, request):
        """Редактирование своих данных."""

        instance = self.request.user
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return response.Response(serializer.data)
