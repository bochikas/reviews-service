from django.urls import include, path
from rest_framework.routers import DefaultRouter

from reviews import views


router = DefaultRouter()
router.register('reviews', views.ReviewViewSet, 'reviews')
router.register('categories', views.CategoryViewSet, 'categories')
router.register('users', views.UserViewSet, 'users')


urlpatterns = [
    path('v1/', include(router.urls)),
    path('register/', views.CreateUserView.as_view(), name='api-create-user')
]
