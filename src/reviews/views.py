from drf_spectacular.utils import extend_schema, OpenApiResponse
from rest_framework import status, response
from rest_framework.views import APIView

from reviews import serializers as api_serializers


class CreateUserView(APIView):
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