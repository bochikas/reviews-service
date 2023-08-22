import uuid

from django.db import models


class UUIDMixin(models.Model):
    """Миксин айди."""

    id = models.UUIDField(primary_key=True, default=uuid.uuid4)

    class Meta:
        abstract = True


class TitleUUIDMixin(UUIDMixin):
    """Миксин."""

    title = models.CharField(verbose_name='Название', max_length=150, help_text='Добавьте название')

    class Meta:
        abstract = True


class CreatedMixin(UUIDMixin):
    """Миксин."""


    class Meta:
        abstract = True



