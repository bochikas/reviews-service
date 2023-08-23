from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from reviews import models as api_models
from reviews.validators import validate_password

User = get_user_model()


class CreateUserSerializer(serializers.ModelSerializer):
    """Сериализатор создания пользователя."""

    email = serializers.EmailField(validators=[UniqueValidator(queryset=User.objects.all())], required=False)

    def validate_password(self, value):
        return validate_password(value, User)

    class Meta:
        model = User
        fields = ('email', 'username', 'first_name', 'last_name', 'password')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = super().create(validated_data)
        password = validated_data.get('password')
        user.set_password(password)
        user.save()
        return user


class IdResponseSerializer(serializers.Serializer):
    """Сериализатор ответа после создания чего-либо."""

    id = serializers.IntegerField(min_value=1)


class ProductSerializer(serializers.ModelSerializer):
    """Сериализатор продукта/услуги."""

    class Meta:
        model = api_models.Product
        fields = '__all__'


class AuthorSerializer(serializers.ModelSerializer):
    """Сериализатор автора обзора."""

    class Meta:
        model = User
        fields = ('id', 'username', 'first_name', 'last_name', 'email', 'is_active', 'last_activity')


class ReviewGetSerializer(serializers.ModelSerializer):
    """Сериализатор просмотра обзоров."""

    product = ProductSerializer()
    author = AuthorSerializer()

    class Meta:
        model = api_models.Review
        fields = '__all__'


class ReviewCreateUpdateSerializer(serializers.ModelSerializer):
    """Сериализатор создания/изменения обзоров."""

    class Meta:
        model = api_models.Review
        fields = ('text', 'recommendation', 'price', 'image', 'score', 'pluses', 'minuses', 'active', 'location')
