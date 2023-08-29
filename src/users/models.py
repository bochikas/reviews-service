import pickle

from django.conf import settings
from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser
from django.core.cache import cache
from django.db import models


class UserManager(BaseUserManager):
    def get_queryset(self):
        return super().get_queryset().filter(is_active=True)


class GenderType(models.IntegerChoices):
    MALE = 1
    FEMALE = 2


class User(AbstractUser):
    """Пользователь."""

    is_company = models.BooleanField(default=False)
    is_verified = models.BooleanField(default=False)
    register_date = models.DateField(verbose_name='Дата регистрации', auto_now_add=True)
    gender = models.CharField(max_length=6, choices=GenderType.choices, verbose_name='Пол')
    photo = models.ImageField(blank=True, null=True, verbose_name='Аватар')
    dob = models.DateField(blank=True, null=True, verbose_name='Дата рождения')
    _last_activity = models.DateTimeField(verbose_name='Последняя активность', null=True)

    objects = UserManager()

    class Meta(AbstractUser.Meta):
        ordering = ('username',)

    @property
    def last_activity(self):
        if val := cache.get(self.get_cache_key()):
            return pickle.loads(val)
        return self._last_activity

    def get_cache_key(self):
        """Формирование ключа для кэша."""

        return f'last_activity::{self.id}'


class Account(models.Model):
    """Аккаунт."""

    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    balance = models.PositiveIntegerField(verbose_name='Баланс', default=0)
    country = models.CharField(verbose_name='Страна', null=True)
    city = models.CharField(verbose_name='Город', null=True)
