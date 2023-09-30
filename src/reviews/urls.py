from django.urls import include, path
from rest_framework.routers import DefaultRouter

from reviews import views


router = DefaultRouter()
router.register('reviews', views.ReviewViewSet, 'reviews')
router.register('categories', views.CategoryViewSet, 'categories')
router.register('users', views.UserViewSet, 'users')


urlpatterns = [
    path('register/', views.CreateUserView.as_view(), name='api-create-user'),
    path('v1/users/me/', views.HandleUserView.as_view(), name='api-user-account'),
    path('v1/', include(router.urls)),
]
