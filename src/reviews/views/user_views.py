from django.contrib.auth import get_user_model
from drf_spectacular.utils import extend_schema, OpenApiResponse
from rest_framework import permissions, response, status, views, viewsets

from reviews.serializers import IdResponseSerializer, UserSerializer, UserEditSerializer
from reviews.services import create_user, update_user

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
        user = create_user(**serializer.validated_data)
        return response.Response({'id': user.id}, status=status.HTTP_201_CREATED)


class HandleUserView(views.APIView):
    """Просмотр и редактирование своих данных."""

    permission_classes = [permissions.IsAuthenticated]
    serializer = UserEditSerializer

    def get_serializer_class(self):  # для drf-spectacular
        return self.serializer

    def get(self, request):
        instance = self.request.user
        serializer = self.serializer(instance)
        return response.Response(serializer.data)

    def patch(self, request):
        instance = self.request.user
        serializer = self.serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        update_user(user=instance, **serializer.validated_data)
        return response.Response(self.serializer(instance).data)


class UserViewSet(viewsets.ReadOnlyModelViewSet):
    """Вьюсет пользователей."""

    queryset = User.objects.active()
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = UserSerializer
