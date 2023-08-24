from django.conf import settings
from django.core.cache import cache
from django.utils.timezone import now


class LastActivityMiddleware:
    """Время последней активности пользователя."""

    def __init__(self, get_response):
        self._get_response = get_response

    def __call__(self, request):
        response = self._get_response(request)
        if request.user.is_authenticated:
            key = request.user.get_cache_key()
            cache.set(key, now(), timeout=settings.USER_LAST_ACTIVITY_CACHE_TIMEOUT)
        return response
