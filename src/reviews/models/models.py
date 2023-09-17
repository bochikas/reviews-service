from django.conf import settings
from django.core.validators import FileExtensionValidator
from django.db import models
from django.utils import timezone

from reviews.models import base_models
from reviews.validators import validate_image_size
from reviews.utils import get_path_upload_image


class Category(base_models.TitleUUIDDeletedMixin, base_models.ActiveMixin):
    """Категория."""

    parent = models.ForeignKey('self', on_delete=models.PROTECT, null=True, blank=True, verbose_name='Надкатегория',
                               related_name='children')
    img = models.ImageField(upload_to=get_path_upload_image, verbose_name='Изображение категории', blank=True,
                            null=True, help_text='Выберите изображение категории', validators=[
                                FileExtensionValidator(allowed_extensions=['jpg', 'png']), validate_image_size])

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        full_path = [self.title]
        k = self.parent
        while k is not None:
            full_path.append(k.title)
            k = k.parent
        return ' -> '.join(full_path[::-1])


class Product(base_models.TitleUUIDDeletedMixin, base_models.ActiveMixin):
    """Продукт/Услуга."""

    category = models.ForeignKey(Category, verbose_name='Категория продукта/услуги', related_name='products',
                                 on_delete=models.PROTECT)

    class Meta:
        verbose_name = 'Продукт/Услуга'
        verbose_name_plural = 'Продукты/Услуги'

    def __str__(self):
        return self.title


class ScoreType(models.IntegerChoices):
    """Вид оценки."""

    AWFUL = 1, 'Ужасно'
    BAD = 2, 'Плохо'
    MEDIUM = 3, 'Средне'
    GOOD = 4, 'Хорошо'
    Perfect = 5, 'Отлично'


class ReviewManager(models.Manager):

    def active(self):
        return self.get_queryset().filter(deleted=False).select_related(
            'product', 'author'
        ).prefetch_related(
            'minuses', 'pluses'
        ).order_by('id')


class Review(base_models.TitleUUIDDeletedMixin):
    """Обзор."""

    product = models.ForeignKey(Product, verbose_name='Продукт', related_name='reviews', on_delete=models.CASCADE)
    text = models.TextField('Текст отзыва', blank=False, help_text='Добавьте текст отзыва')
    recommendation = models.BooleanField(blank=False, default=False, verbose_name='Рекомендуете друзьям?')
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='reviews')
    price = models.IntegerField(verbose_name='Стоимость, например: 100 000 (необязательно)', blank=True, null=True,
                                help_text='сум (только цифры без пробелов и запятых)')
    pub_date = models.DateTimeField(verbose_name='Дата публикации', auto_now_add=True)
    upd_date = models.DateTimeField(auto_now=True, verbose_name='Отредактировано')
    image = models.ImageField(upload_to=get_path_upload_image, verbose_name='Изображение', blank=True, null=True,
                              help_text='Выберите изображение', validators=[
                                    FileExtensionValidator(allowed_extensions=['jpg', 'png']), validate_image_size])
    score = models.PositiveSmallIntegerField(verbose_name='Оценка', choices=ScoreType.choices, default=3)
    pluses = models.ManyToManyField('Plus', verbose_name='Достоинства')
    minuses = models.ManyToManyField('Minus', verbose_name='Недостатки')
    active = models.BooleanField(default=False, verbose_name='Опубликовано')
    draft = models.BooleanField(default=False, verbose_name='Черновик')
    location = models.CharField(max_length=50, verbose_name='Расположение объекта')

    objects = ReviewManager()

    class Meta:
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'
        ordering = ('-pub_date',)

    def __str__(self):
        return self.title


class Plus(base_models.TextMixin, base_models.UUIDMixin):
    """Плюсы."""

    class Meta:
        verbose_name = 'Плюс'
        verbose_name_plural = 'Плюсы'


class Minus(base_models.TextMixin, base_models.UUIDMixin):
    """Минусы."""

    class Meta:
        verbose_name = 'Минус'
        verbose_name_plural = 'Минусы'


class AdditionalImage(base_models.UUIDDeletedMixin):
    """Фото для обзора."""

    review = models.ForeignKey(Review, on_delete=models.CASCADE, related_name='additional_images')
    image = models.ImageField(verbose_name='Фото', upload_to=get_path_upload_image,
                              validators=[FileExtensionValidator(allowed_extensions=['jpg', 'png'])])


class Bookmark(base_models.UUIDDeletedMixin):
    """Закладки."""

    review = models.ForeignKey(Review, on_delete=models.CASCADE, related_name='bookmarks')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='bookmarks')

    def __str__(self):
        return self.review, self.user


class Comment(base_models.UUIDDeletedMixin):
    """Комментарии."""

    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='children')
    review = models.ForeignKey(Review, related_name='comments', verbose_name='Отзыв', on_delete=models.CASCADE)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name='Автор комментария',
                               related_name='comments')
    text = models.TextField('Текст комментария', blank=False, help_text='Добавьте текст комментария')
    created = models.DateTimeField('Дата комментария', auto_now_add=True)
    active = models.BooleanField(default=False, verbose_name='Одобрен?')

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'
        ordering = ('-created',)

    def __str__(self):
        return self.text[:15]


class Subscriptions(base_models.UUIDDeletedMixin):
    """Подписки."""

    user = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name='Подписчик', related_name='subscriptions',
                             on_delete=models.CASCADE)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name='Автор', related_name='subscribers',
                               on_delete=models.CASCADE)
    created = models.DateTimeField(verbose_name='Создано', auto_now_add=True)

    class Meta:
        verbose_name = 'Подписка'
        verbose_name_plural = 'Подписки'
        constraints = [models.UniqueConstraint(fields=['user', 'author'], name='unique subscriptions')]

    def __str__(self):
        return f'Подписчик - {self.user.username}, Автор - {self.author.username}'


class Chat(base_models.UUIDDeletedMixin):
    """Чат."""

    members = models.ManyToManyField(settings.AUTH_USER_MODEL, verbose_name='Участники')

    class Meta:
        verbose_name = 'Чат'
        verbose_name_plural = 'Чаты'


class Message(base_models.UUIDDeletedMixin):
    """Сообщения чата."""

    chat = models.ForeignKey(Chat, on_delete=models.CASCADE)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='messages')
    text = models.TextField(verbose_name='Сообщение')
    pub_date = models.DateTimeField(default=timezone.now)
    read = models.BooleanField(verbose_name='Прочитано', default=False)

    class Meta:
        verbose_name = 'Участник'
        verbose_name_plural = 'Участники'
        ordering = ['-pub_date']

    def __str__(self):
        return self.text
