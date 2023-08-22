from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _


class GenderType(models.IntegerChoices):
    MALE = 1
    FEMALE = 2


class User(AbstractUser):
    """Пользователь."""

    username = models.CharField(_("username"), max_length=150, unique=True,
                                help_text=_(
                                    "Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only."
                                ),
                                validators=[AbstractUser.username_validator],
                                error_messages={
                                    "unique": _("A user with that username already exists."),
                                },
                                null=True, blank=True)
    email = models.EmailField(_("email address"), unique=True)
    is_company = models.BooleanField(default=False)
    is_verified = models.BooleanField(default=False)
    register_date = models.DateField(verbose_name='Дата регистрации', auto_now_add=True)
    last_activity = models.DateTimeField(verbose_name='Последняя активность')
    gender = models.CharField(max_length=6, choices=GenderType.choices, verbose_name='Пол')
    photo = models.ImageField(blank=True, null=True, verbose_name='Аватар')
    dob = models.DateField(blank=True, null=True, verbose_name='Дата рождения')

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []


class Account(models.Model):
    """Аккаунт."""

    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    balance = models.PositiveIntegerField(verbose_name='Баланс', default=0)
    country = models.CharField(verbose_name='Страна', null=True)
    city = models.CharField(verbose_name='Город', null=True)
