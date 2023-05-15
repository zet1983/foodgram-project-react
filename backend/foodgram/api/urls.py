from rest_framework import routers

from django.urls import path, include

from .views import (
    # CategoryViewSet,
    # CommentViewSet,
    # GenreViewSet,
    # ReviewViewSet,
    # TitlesViewSet,
    UsersViewSet,
)

app_name = 'api_v1'

router = routers.DefaultRouter()
router.register('users', UsersViewSet, basename='users')


urlpatterns = [
    path('', include(router.urls)),
    path('', include('djoser.urls')),
    path('auth/', include('djoser.urls.authtoken')),
]
