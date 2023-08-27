from rest_framework.mixins import DestroyModelMixin


class SoftDeleteDestroyModelMixin(DestroyModelMixin):
    """Миксин с 'мягким' удалением."""

    def perform_destroy(self, instance):
        instance.deleted = True
        instance.save()
