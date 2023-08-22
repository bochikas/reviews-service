from django.contrib.auth import password_validation
from django.conf import settings
from django.core.exceptions import ValidationError
from rest_framework import serializers


def validate_image_size(obj):
    """Валидация размера изображения."""

    max_mb = settings.IMAGE_MAX_SIZE_MB
    max_size = max_mb * 1024 * 1024
    if obj.size > max_size:
        raise ValidationError(f'Максимальный размер файла - {max_mb} мб')


def validate_password(password, model):
    """Валидация пароля."""

    try:
        password_validation.validate_password(password=password, user=model)
    except ValidationError as e:
        raise serializers.ValidationError(e)
    return password
