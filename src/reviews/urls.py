from django.urls import include, path
from rest_framework.routers import DefaultRouter

from reviews.views import CreateUserView, ReviewViewSet


router = DefaultRouter()
router.register('reviews', ReviewViewSet, 'reviews')


urlpatterns = [
    path('v1/', include(router.urls)),
    path('register/', CreateUserView.as_view(), name='api-create-user')
]
