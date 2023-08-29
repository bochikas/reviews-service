import uuid

from django.db import models


class UUIDMixin(models.Model):
    """Миксин айди."""

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    class Meta:
        abstract = True


class UUIDDeletedMixin(UUIDMixin):
    """Миксин с полем 'удалено'."""

    deleted = models.BooleanField(default=False)

    class Meta:
        abstract = True


class TitleUUIDDeletedMixin(UUIDDeletedMixin):
    """Миксин с названием."""

    title = models.CharField(verbose_name='Название', max_length=150, help_text='Добавьте название')

    class Meta:
        abstract = True


class ActiveMixin(models.Model):
    """Миксин с полем 'активно'."""

    active = models.BooleanField(default=False)

    class Meta:
        abstract = True


class TextMixin(models.Model):
    """Миксин с полем 'text'."""

    text = models.CharField(max_length=255)

    class Meta:
        abstract = True
