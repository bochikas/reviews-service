import pickle

from celery import shared_task
from django.contrib.auth import get_user_model
from django.core.cache import cache


User = get_user_model()


@shared_task()
def update_users_last_activity():
    to_update = list()
    for user in User.objects.all():
        if user_cache := cache.get(user.get_cache_key()):
            user._last_activity = pickle.loads(user_cache)
            to_update.append(user)
    User.objects.bulk_update(to_update, fields=['_last_activity'])
