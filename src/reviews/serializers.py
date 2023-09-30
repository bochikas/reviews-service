from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from reviews import models as api_models
from reviews.validators import validate_password

User = get_user_model()


class ReviewMinifiedReadSerializer(serializers.ModelSerializer):
    """Сериализатор просмотра обзоров."""

    product_title = serializers.CharField()

    class Meta:
        model = api_models.Review
        fields = ('id', 'product_title', 'title', )


class UserSerializer(serializers.ModelSerializer):
    """Сериализатор пользователей."""

    email = serializers.EmailField(validators=[UniqueValidator(queryset=User.objects.all())], required=False)
    reviews_cnt = serializers.IntegerField()
    reviews = ReviewMinifiedReadSerializer(many=True)

    def validate_password(self, value):
        return validate_password(value, User)

    class Meta:
        model = User
        fields = ('id', 'email', 'username', 'first_name', 'last_name', 'password', 'reviews_cnt', 'reviews')
        extra_kwargs = {'password': {'write_only': True}}


class IdResponseSerializer(serializers.Serializer):
    """Сериализатор ответа после создания чего-либо."""

    id = serializers.IntegerField(min_value=1)


class CategoryReadSerializer(serializers.ModelSerializer):
    """Сериализатор категорий."""

    class Meta:
        model = api_models.Category
        fields = ('id', 'title', 'parent', 'img')


class CategoryWriteSerializer(serializers.ModelSerializer):
    """Сериализатор категорий."""

    class Meta:
        model = api_models.Category
        fields = ('id', 'title', 'parent', 'img')


class ProductSerializer(serializers.ModelSerializer):
    """Сериализатор продукта/услуги."""

    category = CategoryReadSerializer()

    class Meta:
        model = api_models.Product
        fields = '__all__'


class UserEditSerializer(serializers.ModelSerializer):
    """Сериализатор пользователей."""

    class Meta:
        model = User
        fields = ('id', 'username', 'first_name', 'last_name', 'email', 'photo', 'dob', 'gender')
        read_only_fields = ('id', 'username',)


class UserMinifiedSerializer(serializers.ModelSerializer):
    """Сокращенный сериализатор пользователей."""

    class Meta:
        model = User
        fields = ('id', 'email', 'username', 'first_name', 'last_name')


class ReviewReadSerializer(serializers.ModelSerializer):
    """Сериализатор просмотра обзоров."""

    product = ProductSerializer()
    author = UserMinifiedSerializer()

    class Meta:
        model = api_models.Review
        fields = ('id', 'product', 'author', 'title', 'text', 'recommendation', 'price', 'pub_date', 'upd_date',
                  'image', 'score', 'pluses', 'minuses', 'location')


class ReviewWriteSerializer(serializers.ModelSerializer):
    """Сериализатор создания/изменения обзоров."""

    author = serializers.HiddenField(default=serializers.CurrentUserDefault())
    product = serializers.PrimaryKeyRelatedField(queryset=api_models.Product.objects.all())

    class Meta:
        model = api_models.Review
        fields = ('id', 'title', 'text', 'recommendation', 'price', 'image', 'score', 'pluses', 'minuses', 'active',
                  'location', 'product', 'author')
