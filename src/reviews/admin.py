from django.contrib import admin

from reviews.models import Category, Product, Review, Plus, Minus


class PlusesInline(admin.TabularInline):
    model = Review.pluses.through
    verbose_name = 'плюс'
    verbose_name_plural = 'плюсы'


class MinusesInline(admin.TabularInline):
    model = Review.minuses.through
    verbose_name = 'минус'
    verbose_name_plural = 'минусы'


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'deleted', 'active', 'parent', 'img', )


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'deleted', 'active', 'category', )


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('id', 'product', 'author', 'title', 'text', 'recommendation', 'price', 'image', 'score', 'location')
    exclude = ('pluses', 'minuses')
    inlines = (PlusesInline, MinusesInline)


@admin.register(Plus)
class PlusAdmin(admin.ModelAdmin):
    list_display = ('id', 'text', )


@admin.register(Minus)
class MinusAdmin(admin.ModelAdmin):
    list_display = ('id', 'text', )

