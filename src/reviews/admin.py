from django.contrib import admin

from reviews.models import Category, Product, Review

admin.site.register((Category, Product, Review))
