from django.conf import settings
from django.core.exceptions import ValidationError


def validate_image_size(obj):
    max_mb = settings.IMAGE_MAX_SIZE_MB
    max_size = max_mb * 1024 * 1024
    if obj.size > max_size:
        raise ValidationError(f'Максимальный размер файла - {max_mb} мб')
