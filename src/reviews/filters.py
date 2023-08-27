from django_filters import rest_framework as filters

from reviews.models import Review


class ReviewFilter(filters.FilterSet):
    """Фильтр обзоров."""

    author = filters.NumberFilter(field_name='author_id')
    text = filters.CharFilter(field_name='text', lookup_expr='icontains')
    pub_date = filters.DateRangeFilter()

    class Meta:
        fields = ('author', 'text', 'pub_date')
        model = Review
