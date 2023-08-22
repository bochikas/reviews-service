from drf_spectacular.utils import extend_schema
from rest_framework import status, response
from rest_framework.views import APIView

from reviews import serializers as api_serializers


class CreateUserView(APIView):
    """Регистрация пользователй."""

    serializer = api_serializers.CreateUserSerializer

    @extend_schema(request=api_serializers.CreateUserSerializer,
                   responses={status.HTTP_201_CREATED: None,
                              status.HTTP_400_BAD_REQUEST: None})
    def post(self, request):
        serializer = self.serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return response.Response({'id': serializer.instance.id}, status=status.HTTP_201_CREATED)